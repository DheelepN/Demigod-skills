#!/usr/bin/env python3
"""
score_report.py — Generate and save a structured chapter audit report

Takes audit scores as input and produces a formatted report.
Can also read a JSON audit file and re-format it.

Usage:
    # Interactive scoring
    python score_report.py --chapter "Chapter 1: Why It Hurts So Much"

    # From JSON input
    python score_report.py --input audit.json

    # Output formats
    python score_report.py --chapter "Title" --output report.md
    python score_report.py --input audit.json --json
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# ─── Scoring Constants ────────────────────────────────────────────────────────

DIMENSIONS = [
    {
        "key": "voice_authenticity",
        "label": "Voice Authenticity",
        "description": "Opens with scene/confession, immersive My Story, oscillates I/you in Reflection, no LinkedIn sentences",
        "weight": 1,
    },
    {
        "key": "arc_quality",
        "label": "Pain-to-Transformation Arc",
        "description": "Pain entered fully, wrong attempts shown, realization from within, perspective shift not tidy fix, closing reframes",
        "weight": 1,
    },
    {
        "key": "sentence_rhythm",
        "label": "Sentence Rhythm",
        "description": "Mix of short punchy and long flowing, varied paragraph length, rhetorical questions as pivots",
        "weight": 1,
    },
    {
        "key": "imagery_quality",
        "label": "Metaphor & Imagery",
        "description": "Physical/grounded images, specific enough to visualize, no recycled metaphors, min 2 strong images",
        "weight": 1,
    },
    {
        "key": "structural_integrity",
        "label": "Structural Integrity",
        "description": "Sections demarcated, each paragraph has one beat, no filler, within word count target",
        "weight": 1,
    },
    {
        "key": "ai_contamination",
        "label": "AI Pattern Contamination",
        "description": "Clean of AI vocabulary, significance inflation, -ing tack-ons, chatbot residue (5=clean, 1=heavy)",
        "weight": 1,
    },
    {
        "key": "reader_resonance",
        "label": "Reader Resonance",
        "description": "Reader's pain named accurately, 'how did he know' moment present, no condescension, author in-process",
        "weight": 1,
    },
]

VERDICTS = {
    (28, 35): ("PASS", "✓", "Proceed to Humanizer (Module 6D)"),
    (21, 27): ("CONDITIONAL PASS", "~", "Proceed to Humanizer, address Required Fixes after"),
    (0, 20):  ("REVISE", "✗", "Return to Chapter Writer (Module 6B) with fix list"),
}


def get_verdict(total: int) -> tuple:
    for (lo, hi), (label, icon, action) in VERDICTS.items():
        if lo <= total <= hi:
            return label, icon, action
    return "REVISE", "✗", "Return to Chapter Writer"


def score_to_label(score: int) -> str:
    labels = {5: "Excellent", 4: "Good", 3: "Needs work", 2: "Significant issues", 1: "Failing"}
    return labels.get(score, "Unknown")


def build_report(chapter_title: str, scores: dict, word_count: int = 0,
                 target_words: int = 0, notes: dict = None) -> dict:
    notes = notes or {}
    total = sum(scores.get(d["key"], 0) for d in DIMENSIONS)
    max_score = len(DIMENSIONS) * 5
    verdict, icon, action = get_verdict(total)

    required_fixes = []
    recommended = []

    for dim in DIMENSIONS:
        key = dim["key"]
        score = scores.get(key, 0)
        note = notes.get(key, "")
        if score <= 3:
            required_fixes.append({
                "dimension": dim["label"],
                "score": score,
                "note": note or f"Score {score}/5 — {score_to_label(score)}",
            })
        elif score == 4 and note:
            recommended.append({
                "dimension": dim["label"],
                "score": score,
                "note": note,
            })

    return {
        "chapter": chapter_title,
        "timestamp": datetime.now().isoformat(),
        "word_count": word_count,
        "target_words": target_words,
        "scores": {d["key"]: scores.get(d["key"], 0) for d in DIMENSIONS},
        "total": total,
        "max_score": max_score,
        "verdict": verdict,
        "icon": icon,
        "action": action,
        "required_fixes": required_fixes,
        "recommended": recommended,
    }


def format_report(report: dict) -> str:
    lines = []
    lines.append(f"\n{'═' * 60}")
    lines.append(f"  CHAPTER AUDIT — {report['chapter']}")
    if report.get("word_count"):
        wc_line = f"  Words: {report['word_count']:,}"
        if report.get("target_words"):
            wc_line += f" / Target: {report['target_words']:,}"
        lines.append(wc_line)
    lines.append(f"{'═' * 60}")
    lines.append(f"\n  SCORES")
    lines.append(f"  {'─' * 46}")

    for dim in DIMENSIONS:
        key = dim["key"]
        score = report["scores"].get(key, 0)
        bar = "█" * score + "░" * (5 - score)
        lines.append(f"  {dim['label']:<30} {bar}  {score}/5")

    lines.append(f"  {'─' * 46}")
    lines.append(f"  {'OVERALL':<30} {report['total']}/{report['max_score']}")
    lines.append(f"\n  VERDICT: {report['icon']} {report['verdict']}")
    lines.append(f"  Action:  {report['action']}")

    if report["required_fixes"]:
        lines.append(f"\n  {'─' * 46}")
        lines.append(f"  REQUIRED FIXES ({len(report['required_fixes'])}):")
        for i, fix in enumerate(report["required_fixes"], 1):
            lines.append(f"\n  {i}. {fix['dimension']} [{fix['score']}/5]")
            if fix["note"]:
                lines.append(f"     {fix['note']}")

    if report["recommended"]:
        lines.append(f"\n  RECOMMENDED IMPROVEMENTS:")
        for rec in report["recommended"]:
            lines.append(f"  · {rec['dimension']}: {rec['note']}")

    lines.append(f"\n{'═' * 60}\n")
    return "\n".join(lines)


def interactive_score(chapter_title: str) -> dict:
    """Prompt for scores interactively."""
    print(f"\n  Scoring: {chapter_title}\n")
    scores = {}
    notes = {}

    for dim in DIMENSIONS:
        while True:
            try:
                val = input(f"  {dim['label']} [1-5]: ").strip()
                score = int(val)
                if 1 <= score <= 5:
                    scores[dim["key"]] = score
                    if score <= 3:
                        note = input(f"    Issue note (enter to skip): ").strip()
                        if note:
                            notes[dim["key"]] = note
                    break
                else:
                    print("  Enter a number between 1 and 5")
            except (ValueError, EOFError):
                print("  Invalid input")
                break

    wc = input("\n  Chapter word count (enter to skip): ").strip()
    target = input("  Target word count (enter to skip): ").strip()

    return build_report(
        chapter_title,
        scores,
        int(wc) if wc.isdigit() else 0,
        int(target) if target.isdigit() else 0,
        notes,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate chapter audit report")
    parser.add_argument("--chapter", help="Chapter title")
    parser.add_argument("--input", help="Load scores from JSON file")
    parser.add_argument("--output", help="Save report to file")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.input:
        report = json.loads(Path(args.input).read_text())
    elif args.chapter:
        report = interactive_score(args.chapter)
    else:
        print("Error: provide --chapter or --input", file=sys.stderr)
        sys.exit(1)

    if args.json:
        output = json.dumps(report, indent=2)
        print(output)
    else:
        output = format_report(report)
        print(output)

    if args.output:
        Path(args.output).write_text(output if not args.json else json.dumps(report, indent=2))
        print(f"  Saved to: {args.output}")
