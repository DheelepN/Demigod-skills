#!/usr/bin/env python3
"""
validate_concept.py — Validate a concept document for completeness

Checks that a concept document has all required fields before
it enters the book-writer pipeline. Scores completeness and
flags missing or thin sections.

Usage:
    python validate_concept.py <concept.md>
    python validate_concept.py <concept.md> --json
    python validate_concept.py <concept.md> --strict
"""

import sys
import re
import json
import argparse
from pathlib import Path

# ─── Required Fields ──────────────────────────────────────────────────────────

REQUIRED_FIELDS = [
    {
        "key": "working_title",
        "patterns": [r"WORKING TITLE:", r"Title:"],
        "min_words": 2,
        "weight": "required",
        "label": "Working title",
    },
    {
        "key": "logline",
        "patterns": [r"LOGLINE", r"One[- ]sentence", r"Premise:"],
        "min_words": 10,
        "max_words": 30,
        "weight": "required",
        "label": "Logline (≤25 words)",
    },
    {
        "key": "core_question",
        "patterns": [r"CORE QUESTION", r"THE CORE QUESTION", r"Central question"],
        "min_words": 8,
        "weight": "required",
        "label": "Core question",
    },
    {
        "key": "reader",
        "patterns": [r"THE READER", r"Reader:", r"Audience:"],
        "min_words": 15,
        "weight": "required",
        "label": "Reader profile",
    },
    {
        "key": "promise",
        "patterns": [r"THE PROMISE", r"Promise:", r"What they gain"],
        "min_words": 10,
        "weight": "required",
        "label": "The promise",
    },
    {
        "key": "unique_angle",
        "patterns": [r"UNIQUE ANGLE", r"THE UNIQUE ANGLE", r"What makes this different"],
        "min_words": 15,
        "weight": "required",
        "label": "Unique angle",
    },
    {
        "key": "central_tension",
        "patterns": [r"CENTRAL TENSION", r"PARADOX", r"The tension"],
        "min_words": 8,
        "weight": "required",
        "label": "Central tension / paradox",
    },
    {
        "key": "emotional_arc",
        "patterns": [r"EMOTIONAL ARC", r"Arc:", r"Start:", r"Journey:"],
        "min_words": 20,
        "weight": "required",
        "label": "Emotional arc",
    },
    {
        "key": "thematic_clusters",
        "patterns": [r"THEMATIC CLUSTERS", r"Themes:", r"Chapter territories"],
        "min_words": 30,
        "weight": "required",
        "label": "Thematic clusters (7–10)",
    },
    {
        "key": "comparable_books",
        "patterns": [r"COMPARABLE BOOKS", r"Comp titles", r"Similar books"],
        "min_words": 10,
        "weight": "recommended",
        "label": "Comparable books",
    },
    {
        "key": "risks",
        "patterns": [r"RISKS", r"BLIND SPOTS", r"Risks:"],
        "min_words": 10,
        "weight": "recommended",
        "label": "Risks / blind spots",
    },
    {
        "key": "genre",
        "patterns": [r"GENRE:", r"Genre:"],
        "min_words": 1,
        "weight": "required",
        "label": "Genre",
    },
]

# Banned logline words
BANNED_LOGLINE_WORDS = ["journey", "transformation", "discover", "explore", "delve", "embark"]


def find_field(text: str, field: dict) -> tuple[bool, str, int]:
    """Return (found, extracted_text, word_count)."""
    for pattern in field["patterns"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Extract text after this heading until next all-caps heading or end
            start = match.end()
            remainder = text[start:start + 600]
            # Stop at next heading-like line
            stop = re.search(r"\n[A-Z]{3,}[\s:]", remainder)
            extracted = remainder[:stop.start() if stop else 400].strip()
            words = len(extracted.split())
            return True, extracted, words
    return False, "", 0


def validate_logline(text: str) -> list:
    """Check logline specifically for quality."""
    issues = []
    logline_match = re.search(r"LOGLINE[^\n]*\n(.{10,200})", text, re.IGNORECASE)
    if logline_match:
        logline = logline_match.group(1).strip()
        words = len(logline.split())
        if words > 25:
            issues.append(f"Logline is {words} words — should be ≤25")
        for banned in BANNED_LOGLINE_WORDS:
            if banned in logline.lower():
                issues.append(f"Logline contains banned word: '{banned}'")
    return issues


def validate_concept(filepath: str, strict: bool = False) -> dict:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    total_words = len(text.split())

    results = []
    score = 0
    max_score = 0

    for field in REQUIRED_FIELDS:
        found, extracted, word_count = find_field(text, field)
        is_required = field["weight"] == "required"
        field_score = 2 if is_required else 1
        max_score += field_score

        issues = []
        if not found:
            issues.append(f"Field not found")
        else:
            min_words = field.get("min_words", 0)
            max_words = field.get("max_words", 9999)
            if word_count < min_words:
                issues.append(f"Too thin ({word_count} words, min {min_words})")
            if word_count > max_words:
                issues.append(f"Too long ({word_count} words, max {max_words})")

        if not issues:
            score += field_score

        results.append({
            "field": field["label"],
            "key": field["key"],
            "weight": field["weight"],
            "found": found,
            "word_count": word_count,
            "issues": issues,
            "pass": len(issues) == 0,
        })

    # Logline quality check
    logline_issues = validate_logline(text)

    completeness = round((score / max_score) * 100) if max_score else 0
    required_passing = all(r["pass"] for r in results if r["weight"] == "required")

    return {
        "file": str(path),
        "total_words": total_words,
        "score": score,
        "max_score": max_score,
        "completeness_pct": completeness,
        "ready": required_passing and completeness >= 80,
        "fields": results,
        "logline_issues": logline_issues,
    }


def print_report(result: dict):
    ready_icon = "✓" if result["ready"] else "✗"
    print(f"\n{'═' * 60}")
    print(f"  CONCEPT DOCUMENT VALIDATION")
    print(f"  File: {result['file']}")
    print(f"{'═' * 60}")
    print(f"  Completeness: {result['completeness_pct']}%  ({result['score']}/{result['max_score']} points)")
    print(f"  Status: {ready_icon} {'READY for book-writer' if result['ready'] else 'NOT READY — fix required fields'}")

    print(f"\n  {'FIELD':<35} {'STATUS':<12} {'WORDS'}")
    print(f"  {'─' * 55}")

    for field in result["fields"]:
        if field["pass"]:
            status = "✓ ok"
        else:
            status = "✗ " + (field["issues"][0][:20] if field["issues"] else "?")
        req = " *" if field["weight"] == "required" else "  "
        print(f"  {req}{field['field']:<33} {status:<12} {field['word_count']}")

    if result["logline_issues"]:
        print(f"\n  LOGLINE ISSUES:")
        for issue in result["logline_issues"]:
            print(f"    ⚠ {issue}")

    missing = [f for f in result["fields"] if not f["pass"] and f["weight"] == "required"]
    if missing:
        print(f"\n  REQUIRED FIXES ({len(missing)}):")
        for f in missing:
            for issue in f["issues"]:
                print(f"    ✗ {f['field']}: {issue}")

    print(f"\n  (* = required field)")
    print(f"{'═' * 60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("concept_file")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    result = validate_concept(args.concept_file, args.strict)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)
