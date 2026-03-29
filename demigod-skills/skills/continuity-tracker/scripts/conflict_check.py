#!/usr/bin/env python3
"""
conflict_check.py — Check a chapter for continuity conflicts against the log

Scans a chapter text file against the established facts, retired metaphors,
and delivered insights in the continuity log. Surfaces potential conflicts.

Usage:
    python conflict_check.py <chapter_file> [--log log.json]
    python conflict_check.py <chapter_file> [--log log.json] --json
"""

import sys
import re
import json
import argparse
from pathlib import Path

DEFAULT_LOG = "continuity_log.json"

# ─── Conflict Detection Rules ─────────────────────────────────────────────────

# Known fact patterns that might be stated inconsistently
NUMERICAL_PATTERN = re.compile(r'\b(\d+)\s+(years?|months?|days?|chapters?|books?|pages?)\b', re.IGNORECASE)
NAME_PATTERN = re.compile(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b')


def load_log(log_path: str) -> dict:
    path = Path(log_path)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def check_retired_metaphors(chapter_text: str, retired: list) -> list:
    """Find retired metaphors used again in this chapter."""
    conflicts = []
    chapter_lower = chapter_text.lower()
    for metaphor in retired:
        # Check key phrases from the metaphor
        key_words = [w for w in metaphor.lower().split() if len(w) > 4]
        matches = sum(1 for w in key_words if w in chapter_lower)
        if matches >= 2:
            conflicts.append({
                "type": "repeated_metaphor",
                "severity": "medium",
                "detail": f'Retired metaphor may be reused: "{metaphor}"',
                "suggestion": "Use a fresh image — this metaphor was already delivered in a prior chapter",
            })
    return conflicts


def check_repeated_insights(chapter_text: str, insights: dict) -> list:
    """Check if an insight already fully delivered is being re-delivered."""
    conflicts = []
    chapter_lower = chapter_text.lower()

    for ch_num, insight in insights.items():
        # Look for key phrase overlap
        insight_words = [w for w in insight.lower().split() if len(w) > 5]
        if not insight_words:
            continue
        matches = sum(1 for w in insight_words if w in chapter_lower)
        overlap_ratio = matches / len(insight_words) if insight_words else 0

        if overlap_ratio > 0.5:
            conflicts.append({
                "type": "repeated_insight",
                "severity": "medium",
                "detail": f'Insight from Ch.{ch_num} may be re-delivered: "{insight[:60]}..."',
                "suggestion": "Build on this insight rather than restating it — add a new dimension",
            })

    return conflicts


def check_fact_consistency(chapter_text: str, established_facts: list) -> list:
    """Flag when numerical or named facts appear inconsistently."""
    conflicts = []

    # Extract numbers from chapter
    chapter_numbers = NUMERICAL_PATTERN.findall(chapter_text)

    for fact in established_facts:
        # Check if fact contains numbers that contradict chapter
        fact_numbers = NUMERICAL_PATTERN.findall(fact)
        for fn_val, fn_unit in fact_numbers:
            for cn_val, cn_unit in chapter_numbers:
                if cn_unit.rstrip("s") == fn_unit.rstrip("s") and cn_val != fn_val:
                    conflicts.append({
                        "type": "numerical_inconsistency",
                        "severity": "high",
                        "detail": f'Number mismatch: fact says "{fn_val} {fn_unit}", chapter says "{cn_val} {cn_unit}"',
                        "suggestion": f'Verify against established fact: "{fact[:80]}"',
                    })

    return conflicts


def run_conflict_check(chapter_path: str, log_path: str) -> dict:
    chapter_text = Path(chapter_path).read_text(encoding="utf-8")
    log = load_log(log_path)

    result = {
        "chapter_file": chapter_path,
        "log_file": log_path,
        "conflicts": [],
        "warnings": [],
        "clean": True,
    }

    if not log:
        result["warnings"].append("No continuity log found — run log_manager.py init first")
        return result

    # Run checks
    retired = log.get("metaphors", {}).get("retired", [])
    insights = log.get("insights", {})
    facts = log.get("established_facts", [])

    metaphor_conflicts = check_retired_metaphors(chapter_text, retired)
    insight_conflicts = check_repeated_insights(chapter_text, insights)
    fact_conflicts = check_fact_consistency(chapter_text, facts)

    all_conflicts = metaphor_conflicts + insight_conflicts + fact_conflicts

    result["conflicts"] = all_conflicts
    result["clean"] = len(all_conflicts) == 0

    return result


def print_report(result: dict):
    print(f"\n{'═' * 60}")
    print(f"  CONTINUITY CONFLICT CHECK")
    print(f"  Chapter: {result['chapter_file']}")
    print(f"  Log: {result['log_file']}")
    print(f"{'═' * 60}")

    if result.get("warnings"):
        for w in result["warnings"]:
            print(f"\n  ⚠ {w}")

    if result["clean"]:
        print(f"\n  ✓ No conflicts detected. Chapter is consistent with log.\n")
        return

    high = [c for c in result["conflicts"] if c["severity"] == "high"]
    medium = [c for c in result["conflicts"] if c["severity"] == "medium"]

    print(f"\n  Conflicts: {len(result['conflicts'])} ({len(high)} high, {len(medium)} medium)\n")

    for i, conflict in enumerate(result["conflicts"], 1):
        icon = "✗" if conflict["severity"] == "high" else "⚠"
        print(f"  {icon} [{conflict['severity'].upper()}] {conflict['type'].replace('_', ' ').title()}")
        print(f"     {conflict['detail']}")
        print(f"     → {conflict['suggestion']}\n")

    print(f"{'═' * 60}")
    print(f"  Resolve conflicts before updating the continuity log.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("chapter_file")
    parser.add_argument("--log", default=DEFAULT_LOG)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not Path(args.chapter_file).exists():
        print(f"Error: File not found: {args.chapter_file}", file=sys.stderr)
        sys.exit(1)

    result = run_conflict_check(args.chapter_file, args.log)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)
