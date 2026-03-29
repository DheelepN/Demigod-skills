#!/usr/bin/env python3
"""
changelog_gen.py — Generate a changelog by diffing two SKILL.md versions

Compares old and new skill files. Detects added sections, removed sections,
expanded content, and version changes.

Usage:
    python changelog_gen.py <old_SKILL.md> <new_SKILL.md>
    python changelog_gen.py <old_SKILL.md> <new_SKILL.md> --json
    python changelog_gen.py <old_SKILL.md> <new_SKILL.md> --markdown
"""

import sys
import re
import json
from pathlib import Path


def extract_sections(text: str) -> dict:
    """Return dict of {section_title: content}."""
    sections = {}
    current_title = "__preamble__"
    current_lines = []

    for line in text.splitlines():
        heading = re.match(r"^(#{1,3})\s+(.+)", line)
        if heading:
            sections[current_title] = "\n".join(current_lines).strip()
            current_title = heading.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)

    sections[current_title] = "\n".join(current_lines).strip()
    return sections


def get_version(text: str) -> str:
    match = re.search(r"^version:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else "unknown"


def get_description(text: str) -> str:
    match = re.search(r"^description:\s*\|?\s*(.+?)(?=\n\w+:|---)", text, re.DOTALL | re.MULTILINE)
    return match.group(1).strip()[:200] if match else ""


def diff_skills(old_path: str, new_path: str) -> dict:
    old_text = Path(old_path).read_text(encoding="utf-8")
    new_text = Path(new_path).read_text(encoding="utf-8")

    old_sections = extract_sections(old_text)
    new_sections = extract_sections(new_text)

    old_keys = set(old_sections.keys())
    new_keys = set(new_sections.keys())

    added = sorted(new_keys - old_keys - {"__preamble__"})
    removed = sorted(old_keys - new_keys - {"__preamble__"})
    common = old_keys & new_keys

    expanded = []
    modified = []
    unchanged = []

    for key in sorted(common):
        if key == "__preamble__":
            continue
        old_wc = len(old_sections[key].split())
        new_wc = len(new_sections[key].split())
        if old_wc == 0 and new_wc == 0:
            unchanged.append(key)
        elif new_wc > old_wc * 1.3:
            expanded.append({"section": key, "old_words": old_wc, "new_words": new_wc})
        elif old_sections[key] != new_sections[key]:
            modified.append({"section": key, "old_words": old_wc, "new_words": new_wc})
        else:
            unchanged.append(key)

    old_version = get_version(old_text)
    new_version = get_version(new_text)
    old_wc = len(old_text.split())
    new_wc = len(new_text.split())

    return {
        "old_file": old_path,
        "new_file": new_path,
        "version_change": f"{old_version} → {new_version}",
        "word_count_change": f"{old_wc:,} → {new_wc:,} words ({new_wc - old_wc:+,})",
        "added": added,
        "removed": removed,
        "expanded": expanded,
        "modified": modified,
        "unchanged_count": len(unchanged),
    }


def print_changelog(diff: dict):
    print(f"\n{'═' * 60}")
    print(f"  CHANGELOG")
    print(f"  Version: {diff['version_change']}")
    print(f"  Size: {diff['word_count_change']}")
    print(f"{'═' * 60}\n")

    if diff["added"]:
        print(f"  ADDED ({len(diff['added'])} new sections):")
        for s in diff["added"]:
            print(f"    + {s}")
        print()

    if diff["expanded"]:
        print(f"  EXPANDED ({len(diff['expanded'])} sections grown significantly):")
        for s in diff["expanded"]:
            print(f"    ↑ {s['section']}  ({s['old_words']} → {s['new_words']} words)")
        print()

    if diff["modified"]:
        print(f"  MODIFIED ({len(diff['modified'])} sections changed):")
        for s in diff["modified"]:
            print(f"    ~ {s['section']}  ({s['old_words']} → {s['new_words']} words)")
        print()

    if diff["removed"]:
        print(f"  REMOVED ({len(diff['removed'])} sections):")
        for s in diff["removed"]:
            print(f"    - {s}")
        print()

    print(f"  Unchanged sections: {diff['unchanged_count']}")
    print(f"\n{'═' * 60}\n")


def print_markdown_changelog(diff: dict):
    print(f"## Changelog — {diff['version_change']}\n")
    print(f"**Size**: {diff['word_count_change']}\n")

    if diff["added"]:
        print("### Added")
        for s in diff["added"]:
            print(f"- {s}")
        print()

    if diff["expanded"]:
        print("### Expanded")
        for s in diff["expanded"]:
            print(f"- {s['section']} ({s['old_words']} → {s['new_words']} words)")
        print()

    if diff["modified"]:
        print("### Modified")
        for s in diff["modified"]:
            print(f"- {s['section']}")
        print()

    if diff["removed"]:
        print("### Removed")
        for s in diff["removed"]:
            print(f"- {s}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python changelog_gen.py <old_SKILL.md> <new_SKILL.md> [--json|--markdown]")
        sys.exit(1)

    old_path, new_path = sys.argv[1], sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else "--report"

    for p in [old_path, new_path]:
        if not Path(p).exists():
            print(f"Error: File not found: {p}", file=sys.stderr)
            sys.exit(1)

    diff = diff_skills(old_path, new_path)

    if mode == "--json":
        print(json.dumps(diff, indent=2))
    elif mode == "--markdown":
        print_markdown_changelog(diff)
    else:
        print_changelog(diff)
