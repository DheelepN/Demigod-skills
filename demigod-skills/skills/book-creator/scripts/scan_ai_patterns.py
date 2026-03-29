#!/usr/bin/env python3
"""
scan_ai_patterns.py — Scan text for AI writing patterns

Usage:
    python scan_ai_patterns.py <input_file>
    python scan_ai_patterns.py <input_file> --json
    python scan_ai_patterns.py <input_file> --summary

Output:
    Human-readable report of all AI patterns found, with line numbers.
    Use --json for machine-readable output (for audit scripts).
    Use --summary for a count-only view.
"""

import sys
import re
import json
from pathlib import Path

# ─── Pattern Definitions ─────────────────────────────────────────────────────

PATTERNS = {
    "significance_inflation": {
        "label": "Pattern 1 — Significance Inflation",
        "terms": [
            r"\bstands as\b", r"\bserves as\b", r"\bmarks a\b", r"\btestament to\b",
            r"\ba reminder that\b", r"\bpivotal moment\b", r"\bcrucial role\b",
            r"\bvital role\b", r"\bunderscores\b", r"\bhighlights its importance\b",
            r"\breflects broader\b", r"\bsetting the stage for\b", r"\bevolving landscape\b",
            r"\bindel[i]ble mark\b", r"\bdeeply rooted\b", r"\bkey turning point\b",
            r"\bfocal point\b", r"\bmarks a shift\b", r"\bshaping the\b",
        ],
    },
    "promotional_language": {
        "label": "Pattern 4 — Promotional Language",
        "terms": [
            r"\bboasts\b", r"\bvibrant\b", r"\bnestled\b", r"\bbreathtaking\b",
            r"\bgroundbreaking\b", r"\brenowned\b", r"\bstunning\b", r"\bmust-visit\b",
            r"\bmust-read\b", r"\bshowcasing\b", r"\bexemplifies\b",
        ],
    },
    "ing_tack_ons": {
        "label": "Pattern 3 — Superficial -ing Endings",
        "terms": [
            r"\bhighlighting\b", r"\bunderscoring\b", r"\bemphasizing\b",
            r"\bensuring\b", r"\breflecting\b", r"\bsymbolizing\b",
            r"\bcontributing to\b", r"\bcultivating\b", r"\bfostering\b",
            r"\bshowcasing\b", r"\bencompassing\b",
        ],
    },
    "ai_vocabulary": {
        "label": "Pattern 7 — AI Vocabulary Words",
        "terms": [
            r"\bdelve\b", r"\btapestry\b", r"\bmultifaceted\b", r"\bnuanced\b",
            r"\bembark\b", r"\brealm\b", r"\bfoster\b", r"\belevate\b",
            r"\bleverage\b", r"\bnavigate\b", r"\bunpack\b", r"\bholistic\b",
            r"\bsynergy\b", r"\btransformative\b", r"\bimpactful\b", r"\brobust\b",
            r"\bpivotal\b", r"\btestament\b", r"\blandscape\b", r"\bgarner\b",
            r"\bintricate\b", r"\binterplay\b",
        ],
    },
    "copula_avoidance": {
        "label": "Pattern 8 — Copula Avoidance",
        "terms": [
            r"\bserves as\b", r"\bstands as\b", r"\brepresents a\b", r"\bboasts\b",
            r"\bfeatures\b", r"\boffers a\b",
        ],
    },
    "vague_attributions": {
        "label": "Pattern 5 — Vague Attributions",
        "terms": [
            r"\bexperts (say|argue|believe|suggest)\b",
            r"\bindustry (reports|observers)\b",
            r"\bmany believe\b", r"\bsome critics argue\b",
            r"\bit is widely believed\b", r"\bobservers (have|say)\b",
        ],
    },
    "filler_phrases": {
        "label": "Pattern 22 — Filler Phrases",
        "terms": [
            r"\bin order to\b", r"\bdue to the fact that\b", r"\bat this point in time\b",
            r"\bin the event that\b", r"\bhas the ability to\b",
            r"\bit is important to note\b", r"\bat its core\b",
            r"\bin today's world\b", r"\bin conclusion\b",
            r"\bto summarize\b", r"\bit goes without saying\b",
            r"\bneedless to say\b",
        ],
    },
    "hedging_overload": {
        "label": "Pattern 23 — Hedging Overload",
        "terms": [
            r"\bcould potentially\b", r"\bmight possibly\b",
            r"\bit could be argued\b", r"\bpotentially possibly\b",
        ],
    },
    "generic_conclusions": {
        "label": "Pattern 24 — Generic Positive Conclusions",
        "terms": [
            r"\bthe future (looks|is) bright\b", r"\bexciting times (lie |)ahead\b",
            r"\bthis is just the beginning\b", r"\bcontinue this journey\b",
            r"\bthe possibilities are endless\b", r"\btoward excellence\b",
        ],
    },
    "chatbot_artifacts": {
        "label": "Pattern 19 — Chatbot Artifacts",
        "terms": [
            r"\bgreat question\b", r"\bi hope this helps\b",
            r"\blet me know if\b", r"\bfeel free to\b",
            r"\bof course!\b", r"\bcertainly!\b",
            r"\byou'?re absolutely right\b",
        ],
    },
    "em_dash_overuse": {
        "label": "Pattern 13 — Em Dash Overuse",
        "terms": [r"—"],
        "count_threshold": 3,  # flag only if more than N per paragraph
    },
    "negative_parallelism": {
        "label": "Pattern 9 — Negative Parallelism",
        "terms": [
            r"\bit'?s not just (about |)\b.*?it'?s\b",
            r"\bnot (only|merely|just)\b.*?\bbut\b",
        ],
    },
    "false_ranges": {
        "label": "Pattern 12 — False Ranges",
        "terms": [
            r"\bfrom .{5,40} to .{5,40}, from\b",
        ],
    },
    "hyphen_overuse": {
        "label": "Pattern 25 — Hyphenated Word Pair Overuse",
        "terms": [
            r"\bcross-functional\b", r"\bdata-driven\b", r"\bclient-facing\b",
            r"\bdecision-making\b", r"\bwell-known\b", r"\bhigh-quality\b",
            r"\breal-time\b", r"\blong-term\b", r"\bend-to-end\b",
            r"\bthird-party\b",
        ],
    },
}

# ─── DNA Protection Terms (never flag these) ─────────────────────────────────

DNA_PROTECTED_PHRASES = [
    "but here's",
    "the hardest part wasn't",
    "that is what",
    "did to me from the inside",
    "and you start to see",
]

# ─── Scanner ──────────────────────────────────────────────────────────────────

def is_dna_protected(line: str) -> bool:
    line_lower = line.lower()
    return any(phrase in line_lower for phrase in DNA_PROTECTED_PHRASES)


def scan_file(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    results = {
        "file": str(path),
        "total_lines": len(lines),
        "total_words": len(text.split()),
        "findings": [],
        "pattern_counts": {},
        "total_flags": 0,
        "clean": True,
    }

    for pattern_key, pattern_data in PATTERNS.items():
        label = pattern_data["label"]
        terms = pattern_data["terms"]
        threshold = pattern_data.get("count_threshold", 1)
        pattern_findings = []

        for line_num, line in enumerate(lines, start=1):
            if is_dna_protected(line):
                continue

            line_lower = line.lower()
            matched_terms = []

            for term in terms:
                matches = re.findall(term, line_lower)
                if matches:
                    matched_terms.extend(matches)

            if matched_terms:
                # For em dash, only flag if count exceeds threshold in paragraph
                if pattern_key == "em_dash_overuse":
                    count = line.count("—")
                    if count < threshold:
                        continue

                pattern_findings.append({
                    "line": line_num,
                    "text": line.strip()[:120],
                    "matched": list(set(matched_terms)),
                })

        if pattern_findings:
            results["findings"].append({
                "pattern": label,
                "key": pattern_key,
                "count": len(pattern_findings),
                "instances": pattern_findings,
            })
            results["pattern_counts"][pattern_key] = len(pattern_findings)
            results["total_flags"] += len(pattern_findings)
            results["clean"] = False

    return results


def print_report(results: dict):
    print(f"\n{'═' * 60}")
    print(f"  AI PATTERN SCAN REPORT")
    print(f"  File: {results['file']}")
    print(f"  Words: {results['total_words']:,} | Lines: {results['total_lines']:,}")
    print(f"{'═' * 60}")

    if results["clean"]:
        print("\n  ✓ No AI patterns detected. Text is clean.\n")
        return

    print(f"\n  Total flags: {results['total_flags']}")
    print(f"  Patterns triggered: {len(results['findings'])}\n")

    for finding in results["findings"]:
        print(f"  {'─' * 56}")
        print(f"  {finding['pattern']}  ({finding['count']} instance{'s' if finding['count'] > 1 else ''})")
        for instance in finding["instances"][:5]:  # cap at 5 per pattern
            print(f"    Line {instance['line']:>4}: {instance['text'][:90]}")
            print(f"            Matched: {', '.join(instance['matched'][:3])}")
        if len(finding["instances"]) > 5:
            print(f"    ... and {len(finding['instances']) - 5} more")

    print(f"\n{'═' * 60}")
    print(f"  Run humanizer pass to fix {results['total_flags']} flag(s).\n")


def print_summary(results: dict):
    print(f"\n  {results['file']} — {results['total_words']:,} words")
    if results["clean"]:
        print("  ✓ Clean — no AI patterns found\n")
        return
    print(f"  ✗ {results['total_flags']} flags across {len(results['findings'])} patterns\n")
    for finding in results["findings"]:
        print(f"    {str(finding['count']).rjust(3)}x  {finding['pattern']}")
    print()


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scan_ai_patterns.py <input_file> [--json|--summary]")
        sys.exit(1)

    filepath = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "--report"

    results = scan_file(filepath)

    if mode == "--json":
        print(json.dumps(results, indent=2))
    elif mode == "--summary":
        print_summary(results)
    else:
        print_report(results)
