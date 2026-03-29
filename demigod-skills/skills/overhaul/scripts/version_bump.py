#!/usr/bin/env python3
"""
version_bump.py — Bump version number in a SKILL.md file

Usage:
    python version_bump.py <SKILL.md>                  # auto-bump patch
    python version_bump.py <SKILL.md> --minor          # bump minor
    python version_bump.py <SKILL.md> --major          # bump major
    python version_bump.py <SKILL.md> --set 2.1.0      # set specific version
    python version_bump.py <SKILL.md> --dry-run        # preview only
"""

import sys
import re
from pathlib import Path


def parse_version(v: str) -> tuple:
    parts = v.strip().split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {v}")
    return tuple(int(p) for p in parts)


def format_version(major: int, minor: int, patch: int) -> str:
    return f"{major}.{minor}.{patch}"


def bump_version(current: str, bump_type: str) -> str:
    major, minor, patch = parse_version(current)
    if bump_type == "major":
        return format_version(major + 1, 0, 0)
    elif bump_type == "minor":
        return format_version(major, minor + 1, 0)
    else:  # patch
        return format_version(major, minor, patch + 1)


def update_skill_version(filepath: str, new_version: str, dry_run: bool = False) -> dict:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")

    # Find existing version
    version_match = re.search(r"^version:\s*(.+)$", text, re.MULTILINE)
    old_version = version_match.group(1).strip() if version_match else None

    if version_match:
        new_text = re.sub(
            r"^(version:\s*)(.+)$",
            f"\\g<1>{new_version}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        # Insert version after name line
        new_text = re.sub(
            r"^(name:\s*.+)$",
            f"\\g<1>\nversion: {new_version}",
            text,
            count=1,
            flags=re.MULTILINE,
        )

    result = {
        "file": str(path),
        "old_version": old_version or "none",
        "new_version": new_version,
        "dry_run": dry_run,
    }

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
        result["written"] = True
    else:
        result["written"] = False

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python version_bump.py <SKILL.md> [--major|--minor|--patch|--set X.Y.Z] [--dry-run]")
        sys.exit(1)

    filepath = sys.argv[1]
    args = sys.argv[2:]

    bump_type = "patch"
    set_version = None
    dry_run = "--dry-run" in args

    if "--major" in args:
        bump_type = "major"
    elif "--minor" in args:
        bump_type = "minor"
    elif "--set" in args:
        idx = args.index("--set")
        if idx + 1 < len(args):
            set_version = args[idx + 1]

    # Read current version
    path = Path(filepath)
    text = path.read_text(encoding="utf-8")
    version_match = re.search(r"^version:\s*(.+)$", text, re.MULTILINE)
    current = version_match.group(1).strip() if version_match else "1.0.0"

    if set_version:
        new_version = set_version
    else:
        try:
            new_version = bump_version(current, bump_type)
        except ValueError:
            new_version = "2.0.0"

    result = update_skill_version(filepath, new_version, dry_run)

    action = "Would update" if dry_run else "Updated"
    print(f"\n  {action}: {result['file']}")
    print(f"  Version: {result['old_version']} → {result['new_version']}")
    if dry_run:
        print(f"  (dry run — no changes written)\n")
    else:
        print(f"  ✓ Written\n")
