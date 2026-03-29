#!/usr/bin/env python3
"""
bank_formatter.py — Format and validate a research bank

Reads a research bank JSON or markdown file and outputs a
structured, validated bank ready for the book-writer to use.
Also validates quote lengths and source attribution.

Usage:
    python bank_formatter.py <bank.json>
    python bank_formatter.py <bank.json> --chapter 3
    python bank_formatter.py <bank.json> --validate
    python bank_formatter.py <bank.json> --markdown
"""

import sys
import re
import json
import argparse
from pathlib import Path

MAX_QUOTE_WORDS = 30

# ─── Banned / Overexposed Terms ───────────────────────────────────────────────

BANNED_SOURCES = [
    "tony robbins", "brené brown", "marie kondo", "simon sinek",
    "gary vee", "gary vaynerchuk", "oprah",
]

OVEREXPOSED_QUOTES = [
    "be the change you wish to see",
    "the unexamined life is not worth living",
    "insanity is doing the same thing",
    "you miss 100% of the shots",
    "it always seems impossible until it's done",
    "in the middle of difficulty lies opportunity",
    "the only way to do great work",
]


def validate_quote(quote: str) -> list:
    """Return list of issues with a quote."""
    issues = []
    words = quote.split()
    if len(words) > MAX_QUOTE_WORDS:
        issues.append(f"Quote too long ({len(words)} words, max {MAX_QUOTE_WORDS})")

    quote_lower = quote.lower()
    for overexposed in OVEREXPOSED_QUOTES:
        if overexposed in quote_lower:
            issues.append(f"Overexposed quote detected — find something more original")
            break

    return issues


def validate_source(source: str) -> list:
    """Return list of issues with a source attribution."""
    issues = []
    source_lower = source.lower()

    for banned in BANNED_SOURCES:
        if banned in source_lower:
            issues.append(f"Pop-psychology source not aligned with Vivid's voice: {source}")

    if source.lower() in ("unknown", "anonymous", "") :
        issues.append("Source is unknown — verify or remove")

    return issues


def validate_bank(bank: dict) -> dict:
    """Run full validation on a research bank."""
    all_issues = []

    for chapter_key, chapter_data in bank.get("chapters", {}).items():
        chapter_issues = []

        for quote_item in chapter_data.get("quotes", []):
            quote = quote_item.get("quote", "")
            source = quote_item.get("source", "")
            q_issues = validate_quote(quote)
            s_issues = validate_source(source)
            if q_issues or s_issues:
                chapter_issues.append({
                    "chapter": chapter_key,
                    "type": "quote",
                    "content": quote[:60],
                    "issues": q_issues + s_issues,
                })

        for anchor in chapter_data.get("philosophical_anchors", []):
            if not anchor.get("connection"):
                chapter_issues.append({
                    "chapter": chapter_key,
                    "type": "anchor",
                    "content": str(anchor)[:60],
                    "issues": ["Missing 'connection' field — how does this relate to the chapter?"],
                })

        all_issues.extend(chapter_issues)

    return {
        "total_issues": len(all_issues),
        "clean": len(all_issues) == 0,
        "issues": all_issues,
    }


def format_chapter_bank(chapter_key: str, chapter_data: dict) -> str:
    lines = []
    lines.append(f"\n{'─' * 56}")
    lines.append(f"CHAPTER {chapter_key}: {chapter_data.get('title', '')}")
    lines.append(f"Theme: {chapter_data.get('theme', 'Not specified')}")

    anchors = chapter_data.get("philosophical_anchors", [])
    if anchors:
        lines.append(f"\nPhilosophical anchors:")
        for a in anchors:
            thinker = a.get("thinker", "Unknown")
            idea = a.get("idea", "")
            connection = a.get("connection", "")
            lines.append(f"  • {thinker} — {idea}")
            if connection:
                lines.append(f"    → {connection}")

    quotes = chapter_data.get("quotes", [])
    if quotes:
        lines.append(f"\nQuotes ({len(quotes)}):")
        for q in quotes:
            lines.append(f"  \"{q.get('quote', '')}\"")
            lines.append(f"  — {q.get('source', 'Unknown')}")

    research = chapter_data.get("research", [])
    if research:
        lines.append(f"\nResearch / data:")
        for r in research:
            lines.append(f"  • {r.get('finding', '')} [{r.get('source', '')}]")

    opposition = chapter_data.get("opposition", "")
    if opposition:
        lines.append(f"\nConceptual opposition:")
        lines.append(f"  {opposition}")

    notes = chapter_data.get("writing_notes", "")
    if notes:
        lines.append(f"\nWriting notes:")
        lines.append(f"  {notes}")

    return "\n".join(lines)


def print_bank(bank: dict, chapter_filter: int = None):
    print(f"\n{'═' * 60}")
    print(f"  RESEARCH BANK — {bank.get('book_title', 'Unknown Book')}")
    print(f"{'═' * 60}")

    global_anchors = bank.get("global_anchors", [])
    if global_anchors:
        print(f"\nGLOBAL ANCHORS (whole manuscript):")
        for a in global_anchors:
            print(f"  • {a}")

    chapters = bank.get("chapters", {})
    for key, data in sorted(chapters.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0):
        if chapter_filter and int(key) != chapter_filter:
            continue
        print(format_chapter_bank(key, data))

    print(f"\n{'═' * 60}")
    print(f"  Chapters in bank: {len(chapters)}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bank_file")
    parser.add_argument("--chapter", type=int, help="Show specific chapter only")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.bank_file)
    if not path.exists():
        print(f"Error: File not found: {args.bank_file}", file=sys.stderr)
        sys.exit(1)

    bank = json.loads(path.read_text(encoding="utf-8"))

    if args.validate:
        result = validate_bank(bank)
        if result["clean"]:
            print(f"\n  ✓ Research bank is clean — {len(bank.get('chapters', {}))} chapters validated\n")
        else:
            print(f"\n  ✗ {result['total_issues']} issue(s) found:\n")
            for issue in result["issues"]:
                print(f"  Ch.{issue['chapter']} [{issue['type']}]: {issue['content']}")
                for i in issue["issues"]:
                    print(f"    → {i}")
            print()
    elif args.json:
        print(json.dumps(bank, indent=2))
    else:
        print_bank(bank, args.chapter)
