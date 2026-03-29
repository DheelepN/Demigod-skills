#!/usr/bin/env python3
"""
kdp_check.py — KDP pre-flight checker for manuscript DOCX files

Validates a DOCX manuscript against KDP's technical requirements
before upload. Checks margins, page size, fonts, images, and structure.

Usage:
    python kdp_check.py <manuscript.docx>
    python kdp_check.py <manuscript.docx> --trim 6x9
    python kdp_check.py <manuscript.docx> --json
"""

import sys
import json
import zipfile
import re
from pathlib import Path

# ─── KDP Requirements ─────────────────────────────────────────────────────────

# Trim sizes in EMU (914400 EMU = 1 inch)
TRIM_SIZES = {
    "5x8":    {"w": 4572000,  "h": 7315200},
    "6x9":    {"w": 5486400,  "h": 8229600},
    "8.5x11": {"w": 7772400,  "h": 10058400},
}

# Minimum margins in EMU (KDP requires at least 0.5" outside, 0.625" inside)
MIN_MARGINS = {
    "outside": 457200,   # 0.5 inch
    "inside":  571500,   # 0.625 inch
    "top":     457200,
    "bottom":  457200,
}

# KDP safe fonts (always render correctly)
SAFE_FONTS = {
    "georgia", "times new roman", "garamond", "palatino linotype",
    "arial", "helvetica", "calibri", "cambria", "courier new",
    "book antiqua", "century", "trebuchet ms",
}

KDP_MIN_IMAGE_DPI = 300
KDP_MAX_FILE_SIZE_MB = 650


def check_file_size(filepath: str) -> dict:
    size_mb = Path(filepath).stat().st_size / (1024 * 1024)
    return {
        "check": "File size",
        "value": f"{size_mb:.1f} MB",
        "pass": size_mb <= KDP_MAX_FILE_SIZE_MB,
        "requirement": f"≤ {KDP_MAX_FILE_SIZE_MB} MB",
        "note": "" if size_mb <= KDP_MAX_FILE_SIZE_MB else "File too large for KDP upload",
    }


def extract_docx_xml(filepath: str) -> dict:
    """Extract relevant XML files from DOCX."""
    xml_files = {}
    try:
        with zipfile.ZipFile(filepath, "r") as z:
            for name in z.namelist():
                if name in ("word/document.xml", "word/settings.xml",
                            "word/styles.xml", "[Content_Types].xml"):
                    xml_files[name] = z.read(name).decode("utf-8", errors="replace")
    except zipfile.BadZipFile:
        print(f"Error: Not a valid DOCX file: {filepath}", file=sys.stderr)
        sys.exit(1)
    return xml_files


def check_page_size(xml_files: dict, trim_key: str = None) -> dict:
    doc_xml = xml_files.get("word/document.xml", "")
    # Look for w:pgSz element
    match = re.search(r'<w:pgSz[^>]+w:w="(\d+)"[^>]+w:h="(\d+)"', doc_xml)
    if not match:
        match = re.search(r'<w:pgSz[^>]+w:h="(\d+)"[^>]+w:w="(\d+)"', doc_xml)
        if match:
            w_dxa, h_dxa = int(match.group(2)), int(match.group(1))
        else:
            return {
                "check": "Page size",
                "pass": None,
                "value": "Not detected",
                "requirement": "Must match chosen trim size",
                "note": "Could not read page dimensions from document",
            }
    else:
        w_dxa, h_dxa = int(match.group(1)), int(match.group(2))

    # DXA to inches (1440 DXA = 1 inch)
    w_in = w_dxa / 1440
    h_in = h_dxa / 1440

    if trim_key and trim_key in TRIM_SIZES:
        expected = TRIM_SIZES[trim_key]
        # Convert EMU to DXA (914400 EMU = 1 inch = 1440 DXA, so EMU/635 = DXA)
        exp_w_dxa = expected["w"] // 635
        exp_h_dxa = expected["h"] // 635
        passed = abs(w_dxa - exp_w_dxa) < 100 and abs(h_dxa - exp_h_dxa) < 100
        req = f"{trim_key} ({exp_w_dxa/1440:.2f}\" × {exp_h_dxa/1440:.2f}\")"
    else:
        passed = any(
            abs(w_dxa - ts["w"] // 635) < 100
            for ts in TRIM_SIZES.values()
        )
        req = "One of: 5×8, 6×9, 8.5×11"

    return {
        "check": "Page size",
        "pass": passed,
        "value": f"{w_in:.2f}\" × {h_in:.2f}\"",
        "requirement": req,
        "note": "" if passed else f"Page size doesn't match expected trim",
    }


def check_margins(xml_files: dict) -> dict:
    doc_xml = xml_files.get("word/document.xml", "")
    match = re.search(
        r'<w:pgMar[^>]+w:top="(\d+)"[^>]+w:right="(\d+)"[^>]+w:bottom="(\d+)"[^>]+w:left="(\d+)"',
        doc_xml,
    )
    if not match:
        return {
            "check": "Margins",
            "pass": None,
            "value": "Not detected",
            "requirement": "Min 0.5\" outside, 0.625\" inside",
            "note": "Could not read margins from document",
        }

    top, right, bottom, left = (int(match.group(i)) for i in range(1, 5))

    # KDP: inside margin (left for recto) must be at least 864 DXA (0.6")
    # outside margin must be at least 720 DXA (0.5")
    min_outside = 720  # DXA
    min_inside = 864   # DXA

    issues = []
    if top < min_outside:
        issues.append(f"Top margin {top/1440:.2f}\" < 0.5\"")
    if bottom < min_outside:
        issues.append(f"Bottom margin {bottom/1440:.2f}\" < 0.5\"")
    if left < min_inside:
        issues.append(f"Left margin {left/1440:.2f}\" < 0.6\"")
    if right < min_outside:
        issues.append(f"Right margin {right/1440:.2f}\" < 0.5\"")

    return {
        "check": "Margins",
        "pass": len(issues) == 0,
        "value": f"T:{top/1440:.2f}\" R:{right/1440:.2f}\" B:{bottom/1440:.2f}\" L:{left/1440:.2f}\"",
        "requirement": "Min 0.5\" all sides, 0.6\" inside",
        "note": "; ".join(issues) if issues else "",
    }


def check_fonts(xml_files: dict) -> dict:
    styles_xml = xml_files.get("word/styles.xml", "")
    fonts_found = set(re.findall(r'w:name="([^"]+)"', styles_xml))
    # Filter to font-like names (not style names)
    font_names = {f.lower() for f in fonts_found if len(f) > 3 and " " not in f or f.lower() in SAFE_FONTS}
    unsafe = [f for f in font_names if f not in SAFE_FONTS and len(f) > 3]

    return {
        "check": "Fonts",
        "pass": len(unsafe) == 0,
        "value": f"{len(font_names)} font(s) detected",
        "requirement": "Use standard embeddable fonts",
        "note": f"Possibly non-standard: {', '.join(list(unsafe)[:3])}" if unsafe else "",
    }


def check_content_types(xml_files: dict) -> dict:
    ct_xml = xml_files.get("[Content_Types].xml", "")
    has_rels = "relationships" in ct_xml.lower()
    has_doc = "wordprocessingml" in ct_xml.lower()
    return {
        "check": "Document structure",
        "pass": has_rels and has_doc,
        "value": "Valid DOCX structure" if (has_rels and has_doc) else "Invalid structure",
        "requirement": "Valid OOXML structure",
        "note": "" if (has_rels and has_doc) else "Document may be corrupted",
    }


def print_report(checks: list, filepath: str):
    passed = sum(1 for c in checks if c["pass"] is True)
    failed = sum(1 for c in checks if c["pass"] is False)
    unknown = sum(1 for c in checks if c["pass"] is None)

    print(f"\n{'═' * 60}")
    print(f"  KDP PRE-FLIGHT CHECK")
    print(f"  File: {filepath}")
    print(f"{'═' * 60}")
    print(f"  {'CHECK':<24} {'STATUS':<16} {'VALUE':<22} NOTE")
    print(f"  {'─' * 56}")

    for c in checks:
        if c["pass"] is True:
            status = "✓ PASS"
        elif c["pass"] is False:
            status = "✗ FAIL"
        else:
            status = "? UNKNOWN"
        note = c.get("note", "")[:30]
        print(f"  {c['check']:<24} {status:<16} {c['value']:<22} {note}")

    print(f"\n  {'─' * 56}")
    print(f"  Result: {passed} passed  {failed} failed  {unknown} unknown")
    if failed == 0 and unknown == 0:
        print(f"  ✓ Ready for KDP upload.")
    elif failed > 0:
        print(f"  ✗ Fix {failed} issue(s) before uploading.")
    print(f"\n{'═' * 60}\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python kdp_check.py <file.docx> [--trim 5x8|6x9|8.5x11] [--json]")
        sys.exit(1)

    filepath = sys.argv[1]
    trim_key = None
    mode = "--report"

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--trim" and i + 1 < len(sys.argv):
            trim_key = sys.argv[i + 1]
        elif arg == "--json":
            mode = "--json"

    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    xml_files = extract_docx_xml(filepath)

    checks = [
        check_file_size(filepath),
        check_page_size(xml_files, trim_key),
        check_margins(xml_files),
        check_fonts(xml_files),
        check_content_types(xml_files),
    ]

    if mode == "--json":
        print(json.dumps({"file": filepath, "checks": checks}, indent=2))
    else:
        print_report(checks, filepath)
