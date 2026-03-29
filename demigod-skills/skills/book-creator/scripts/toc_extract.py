#!/usr/bin/env python3
"""
toc_extract.py — Extract table of contents from a manuscript

Detects chapter headings, part dividers, and section structure.
Outputs formatted TOC or JSON.

Usage:
    python toc_extract.py <manuscript_file>
    python toc_extract.py <manuscript_file> --json
    python toc_extract.py <manuscript_file> --markdown
"""

import sys
import re
import json
from pathlib import Path

PART_PATTERN = re.compile(r"^(Part\s+(I{1,4}|[0-9]+)|PART\s+\w+)[:\s]?", re.IGNORECASE)
CHAPTER_PATTERN = re.compile(r"^(Chapter\s+\d+|CHAPTER\s+\d+|#{1,2}\s+Chapter)", re.IGNORECASE)
INTRO_PATTERN = re.compile(r"^(Introduction|Foreword|Preface|Prologue|How to Use)", re.IGNORECASE)
OUTRO_PATTERN = re.compile(r"^(Conclusion|Epilogue|Afterword|About the Author|Acknowledgments)", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"^#{1,3}\s+(.+)")


def extract_toc(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    lines = path.read_text(encoding="utf-8").splitlines()

    toc = {
        "front_matter": [],
        "parts": [],
        "back_matter": [],
        "ungrouped_chapters": [],
    }

    current_part = None
    chapter_num = 0

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue

        if INTRO_PATTERN.match(stripped):
            toc["front_matter"].append({
                "title": stripped.lstrip("#").strip(),
                "line": line_num,
                "type": "front",
            })

        elif OUTRO_PATTERN.match(stripped):
            toc["back_matter"].append({
                "title": stripped.lstrip("#").strip(),
                "line": line_num,
                "type": "back",
            })

        elif PART_PATTERN.match(stripped):
            current_part = {
                "title": stripped.lstrip("#").strip(),
                "line": line_num,
                "chapters": [],
            }
            toc["parts"].append(current_part)

        elif CHAPTER_PATTERN.match(stripped) or (HEADING_PATTERN.match(stripped) and stripped.startswith("#")):
            chapter_num += 1
            title = stripped.lstrip("#").strip()
            chapter = {
                "number": chapter_num,
                "title": title,
                "line": line_num,
            }
            if current_part:
                current_part["chapters"].append(chapter)
            else:
                toc["ungrouped_chapters"].append(chapter)

    return toc


def print_toc(toc: dict):
    print(f"\n{'═' * 60}")
    print(f"  TABLE OF CONTENTS")
    print(f"{'═' * 60}\n")

    if toc["front_matter"]:
        for item in toc["front_matter"]:
            print(f"  {item['title']}")
        print()

    if toc["parts"]:
        for part in toc["parts"]:
            print(f"  {part['title'].upper()}")
            for ch in part["chapters"]:
                print(f"    Chapter {ch['number']}: {ch['title']}")
            print()
    elif toc["ungrouped_chapters"]:
        for ch in toc["ungrouped_chapters"]:
            print(f"  Chapter {ch['number']}: {ch['title']}")
        print()

    if toc["back_matter"]:
        for item in toc["back_matter"]:
            print(f"  {item['title']}")
        print()

    total = sum(len(p["chapters"]) for p in toc["parts"]) + len(toc["ungrouped_chapters"])
    print(f"  Total chapters: {total}")
    print(f"{'═' * 60}\n")


def print_markdown_toc(toc: dict):
    print("## Table of Contents\n")
    for item in toc["front_matter"]:
        print(f"- {item['title']}")
    if toc["parts"]:
        for part in toc["parts"]:
            print(f"\n### {part['title']}")
            for ch in part["chapters"]:
                print(f"- Chapter {ch['number']}: {ch['title']}")
    else:
        for ch in toc["ungrouped_chapters"]:
            print(f"- Chapter {ch['number']}: {ch['title']}")
    if toc["back_matter"]:
        print()
        for item in toc["back_matter"]:
            print(f"- {item['title']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python toc_extract.py <file> [--json|--markdown]")
        sys.exit(1)

    filepath = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "--report"

    toc = extract_toc(filepath)

    if mode == "--json":
        print(json.dumps(toc, indent=2))
    elif mode == "--markdown":
        print_markdown_toc(toc)
    else:
        print_toc(toc)
