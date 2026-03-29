#!/usr/bin/env python3
"""
word_count.py — Word count analyzer for book manuscripts

Counts words per chapter/section and compares against KDP targets.
Detects chapter boundaries automatically from heading patterns.

Usage:
    python word_count.py <manuscript_file>
    python word_count.py <manuscript_file> --target <short|medium|full>
    python word_count.py <manuscript_file> --json
"""

import sys
import re
import json
from pathlib import Path

# ─── KDP Word Count Targets ───────────────────────────────────────────────────

TARGETS = {
    "short":  {"per_chapter": (1500, 2000),  "total": (10000, 20000)},
    "medium": {"per_chapter": (2000, 3500),  "total": (20000, 50000)},
    "full":   {"per_chapter": (3500, 5000),  "total": (50000, 100000)},
}

# Chapter heading patterns
CHAPTER_PATTERNS = [
    re.compile(r"^#{1,2}\s+(Chapter\s+\d+|CHAPTER\s+\d+)", re.IGNORECASE),
    re.compile(r"^Chapter\s+\d+[:\s]", re.IGNORECASE),
    re.compile(r"^CHAPTER\s+\d+", re.IGNORECASE),
    re.compile(r"^#{1,2}\s+\w"),  # any h1/h2
]

SECTION_PATTERNS = [
    re.compile(r"^My Story", re.IGNORECASE),
    re.compile(r"^My Reflection", re.IGNORECASE),
    re.compile(r"^#{3}\s+", re.IGNORECASE),  # h3
]


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def is_chapter_heading(line: str) -> bool:
    return any(p.match(line.strip()) for p in CHAPTER_PATTERNS)


def is_section_heading(line: str) -> bool:
    return any(p.match(line.strip()) for p in SECTION_PATTERNS)


def parse_manuscript(filepath: str) -> list:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    chapters = []
    current_chapter = None
    current_section = None
    front_matter_lines = []
    in_front_matter = True

    for line in lines:
        if is_chapter_heading(line):
            if current_chapter:
                # save previous chapter
                if current_section:
                    current_chapter["sections"].append(current_section)
                    current_section = None
                chapters.append(current_chapter)

            current_chapter = {
                "title": line.strip().lstrip("#").strip(),
                "content": "",
                "sections": [],
                "word_count": 0,
            }
            in_front_matter = False

        elif is_section_heading(line) and current_chapter:
            if current_section:
                current_chapter["sections"].append(current_section)
            current_section = {
                "title": line.strip().lstrip("#").strip(),
                "content": "",
                "word_count": 0,
            }

        else:
            if in_front_matter:
                front_matter_lines.append(line)
            elif current_section:
                current_section["content"] += line + "\n"
            elif current_chapter:
                current_chapter["content"] += line + "\n"

    # flush last chapter/section
    if current_section and current_chapter:
        current_chapter["sections"].append(current_section)
    if current_chapter:
        chapters.append(current_chapter)

    # calculate word counts
    for ch in chapters:
        section_words = sum(count_words(s["content"]) for s in ch["sections"])
        for s in ch["sections"]:
            s["word_count"] = count_words(s["content"])
        ch["word_count"] = count_words(ch["content"]) + section_words

    front_matter_text = "\n".join(front_matter_lines)
    front_matter_words = count_words(front_matter_text)

    return chapters, front_matter_words


def assess_chapter(chapter: dict, target_range: tuple) -> str:
    wc = chapter["word_count"]
    lo, hi = target_range
    if wc < lo * 0.8:
        return "⚠ SHORT"
    elif wc > hi * 1.2:
        return "⚠ LONG"
    elif lo <= wc <= hi:
        return "✓ ON TARGET"
    else:
        return "~ CLOSE"


def print_report(chapters: list, front_matter_words: int, target_key: str = None):
    total_words = sum(ch["word_count"] for ch in chapters) + front_matter_words
    target = TARGETS.get(target_key) if target_key else None
    target_range = target["per_chapter"] if target else None

    print(f"\n{'═' * 60}")
    print(f"  MANUSCRIPT WORD COUNT REPORT")
    print(f"{'═' * 60}")
    print(f"  Total manuscript: {total_words:,} words")
    print(f"  Chapters detected: {len(chapters)}")
    if front_matter_words:
        print(f"  Front matter: {front_matter_words:,} words")

    if target:
        tlo, thi = target["total"]
        clo, chi = target["per_chapter"]
        status = "✓" if tlo <= total_words <= thi else "⚠"
        print(f"  Target ({target_key}): {tlo:,}–{thi:,} words total | {clo:,}–{chi:,} per chapter")
        print(f"  Overall status: {status} {'ON TARGET' if tlo <= total_words <= thi else 'OFF TARGET'}")

    print(f"\n  {'CHAPTER':<40} {'WORDS':>7}  {'STATUS':<14}  SECTIONS")
    print(f"  {'─' * 56}")

    for ch in chapters:
        status = assess_chapter(ch, target_range) if target_range else ""
        sections_info = ", ".join(
            f"{s['title'][:15]} ({s['word_count']:,}w)" for s in ch["sections"]
        ) if ch["sections"] else "—"
        print(f"  {ch['title'][:38]:<40} {ch['word_count']:>7,}  {status:<14}  {sections_info[:30]}")

    print(f"\n{'═' * 60}\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python word_count.py <file> [--target short|medium|full] [--json]")
        sys.exit(1)

    filepath = sys.argv[1]
    target_key = None
    mode = "--report"

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--target" and i + 1 < len(sys.argv):
            target_key = sys.argv[i + 1]
        elif arg == "--json":
            mode = "--json"

    chapters, front_matter_words = parse_manuscript(filepath)

    if mode == "--json":
        output = {
            "total_words": sum(ch["word_count"] for ch in chapters) + front_matter_words,
            "front_matter_words": front_matter_words,
            "chapter_count": len(chapters),
            "chapters": chapters,
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(chapters, front_matter_words, target_key)
