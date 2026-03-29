#!/usr/bin/env python3
"""
dna_scan.py — Scan text for Vivid's protected DNA constructions

Identifies Vivid's authentic signature constructions that must NOT be
stripped by the humanizer. Marks them so the pattern elimination pass
knows to skip them.

Usage:
    python dna_scan.py <input_file>
    python dna_scan.py <input_file> --json
"""

import sys
import re
import json
from pathlib import Path

# ─── DNA Constructions to Protect ────────────────────────────────────────────

DNA_RULES = [
    {
        "name": "Signature Phrases",
        "description": "Vivid's recurring voice markers — never strip",
        "patterns": [
            r"\bbut here'?s\b",
            r"\bthe hardest part wasn'?t\b",
            r"\bthat is what .{3,40} did to me from the inside\b",
            r"\band you start to see\b",
        ],
    },
    {
        "name": "Protected Negative Parallelisms",
        "description": "Grounded in specific experience — not generic contrast",
        "patterns": [
            r"\bnot the .{5,60}, but what\b",
            r"\bnot the .{5,60}, but the\b",
        ],
        "note": "Only protect if both sides reference concrete, specific experience",
    },
    {
        "name": "Protected Em Dashes (Emotional Weight)",
        "description": "Em dashes around emotionally significant phrases",
        "patterns": [
            r"— that .{3,50} —",
            r"— [a-z].{3,50} —",
        ],
        "note": "Only protect when em dash is around a named emotional moment",
    },
    {
        "name": "Physical Imagery",
        "description": "Vivid's grounded physical metaphors — never flatten",
        "patterns": [
            r"\bpressed down on my chest\b",
            r"\bknife that cut\b",
            r"\bscraps of attention\b",
            r"\binvisible chains\b",
            r"\bdeafening scream inside\b",
            r"\bsuffocating grip\b",
            r"\bunraveling\b",
        ],
    },
    {
        "name": "Protected Elevated Vocabulary",
        "description": "Elevated words used to name felt experience — not decoration",
        "patterns": [
            r"\binsidious\b", r"\bimperceptibly\b", r"\bagonizing\b",
            r"\bdesolate\b", r"\bconspicuously\b", r"\bgrotesque\b",
            r"\bincessant\b", r"\bsuffocating\b",
        ],
        "note": "Protect only when modifying a specific felt experience",
    },
    {
        "name": "Reframe Closings",
        "description": "Single-sentence reframe closings — core Vivid structure",
        "patterns": [
            r"^[A-Z].{20,120}\.$",  # standalone short paragraph (reframe closing)
        ],
        "note": "Flag for review — Claude determines if it's a reframe closing",
    },
]

# ─── Scanner ──────────────────────────────────────────────────────────────────

def scan_dna(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    results = {
        "file": str(path),
        "total_lines": len(lines),
        "protected_constructions": [],
        "total_protected": 0,
    }

    for rule in DNA_RULES:
        rule_findings = []
        for line_num, line in enumerate(lines, start=1):
            for pattern in rule["patterns"]:
                if re.search(pattern, line, re.IGNORECASE):
                    rule_findings.append({
                        "line": line_num,
                        "text": line.strip()[:120],
                        "note": rule.get("note", ""),
                    })
                    break  # one match per line per rule is enough

        if rule_findings:
            results["protected_constructions"].append({
                "rule": rule["name"],
                "description": rule["description"],
                "count": len(rule_findings),
                "instances": rule_findings,
            })
            results["total_protected"] += len(rule_findings)

    return results


def print_dna_report(results: dict):
    print(f"\n{'═' * 60}")
    print(f"  DNA PROTECTION SCAN")
    print(f"  File: {results['file']}")
    print(f"{'═' * 60}")

    if results["total_protected"] == 0:
        print("\n  No protected DNA constructions found.\n")
        print("  This is normal for non-Vivid text or early drafts.\n")
        return

    print(f"\n  Protected constructions found: {results['total_protected']}")
    print(f"  These will be EXEMPT from AI pattern elimination.\n")

    for item in results["protected_constructions"]:
        print(f"  {'─' * 56}")
        print(f"  ✓ PROTECT: {item['rule']}  ({item['count']} instance{'s' if item['count'] > 1 else ''})")
        print(f"    {item['description']}")
        for inst in item["instances"][:3]:
            print(f"    Line {inst['line']:>4}: {inst['text'][:90]}")
            if inst.get("note"):
                print(f"            Note: {inst['note']}")

    print(f"\n{'═' * 60}")
    print(f"  Mark these {results['total_protected']} line(s) as protected")
    print(f"  before running scan_ai_patterns.py.\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dna_scan.py <input_file> [--json]")
        sys.exit(1)

    filepath = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "--report"

    results = scan_dna(filepath)

    if mode == "--json":
        print(json.dumps(results, indent=2))
    else:
        print_dna_report(results)
