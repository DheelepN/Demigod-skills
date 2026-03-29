#!/usr/bin/env python3
"""
skill_parser.py — Parse and analyze a SKILL.md file

Extracts frontmatter, sections, version, word count, and structural
metrics. Used by the overhaul skill as the first diagnostic step.

Usage:
    python skill_parser.py <SKILL.md>
    python skill_parser.py <SKILL.md> --json
    python skill_parser.py <SKILL.md> --sections
"""

import sys
import re
import json
from pathlib import Path

# ─── Parser ───────────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (meta, body)."""
    if not text.startswith("---"):
        return {}, text

    end = text.find("---", 3)
    if end == -1:
        return {}, text

    yaml_block = text[3:end].strip()
    body = text[end + 3:].strip()

    meta = {}
    for line in yaml_block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key == "description":
                # multiline description — grab until next key
                meta[key] = value
            else:
                meta[key] = value

    # Handle multiline description
    desc_match = re.search(r"description:\s*\|(.+?)(?=\n\w+:|$)", yaml_block, re.DOTALL)
    if desc_match:
        meta["description"] = desc_match.group(1).strip()

    return meta, body


def extract_sections(body: str) -> list:
    """Extract all ## and ### sections with their content."""
    sections = []
    lines = body.splitlines()
    current = None

    for line in lines:
        h2 = re.match(r"^## (.+)", line)
        h3 = re.match(r"^### (.+)", line)

        if h2:
            if current:
                sections.append(current)
            current = {
                "level": 2,
                "title": h2.group(1).strip(),
                "content": "",
                "word_count": 0,
                "subsections": [],
            }
        elif h3 and current:
            # Count words in current section before starting subsection
            sub = {
                "level": 3,
                "title": h3.group(1).strip(),
                "content": "",
                "word_count": 0,
            }
            current["subsections"].append(sub)
        elif current:
            if current["subsections"]:
                current["subsections"][-1]["content"] += line + "\n"
            else:
                current["content"] += line + "\n"

    if current:
        sections.append(current)

    # Calculate word counts
    for sec in sections:
        sec["word_count"] = len(sec["content"].split())
        for sub in sec.get("subsections", []):
            sub["word_count"] = len(sub["content"].split())

    return sections


def detect_issues(meta: dict, body: str, sections: list) -> list:
    """Detect potential skill quality issues."""
    issues = []

    # No version
    if "version" not in meta:
        issues.append({
            "severity": "low",
            "issue": "No version number in frontmatter",
            "fix": "Add `version: 1.0.0` to frontmatter",
        })

    # Description too short
    desc = meta.get("description", "")
    if len(desc) < 50:
        issues.append({
            "severity": "medium",
            "issue": f"Description too short ({len(desc)} chars) — won't trigger reliably",
            "fix": "Expand description to include trigger phrases and use cases",
        })

    if len(desc) > 400:
        issues.append({
            "severity": "low",
            "issue": f"Description very long ({len(desc)} chars) — may be truncated",
            "fix": "Trim to under 300 chars while keeping key trigger phrases",
        })

    # No output format defined
    output_keywords = ["output", "format", "deliver", "result", "produce"]
    has_output_section = any(
        any(kw in sec["title"].lower() for kw in output_keywords)
        for sec in sections
    )
    body_lower = body.lower()
    has_output_mention = any(kw in body_lower for kw in output_keywords)

    if not has_output_section and not has_output_mention:
        issues.append({
            "severity": "high",
            "issue": "No output format defined",
            "fix": "Add an OUTPUT section with a concrete template",
        })

    # No error handling
    error_keywords = ["error", "fail", "if not", "missing", "invalid", "edge case"]
    has_error_handling = any(kw in body_lower for kw in error_keywords)
    if not has_error_handling:
        issues.append({
            "severity": "medium",
            "issue": "No error handling or edge case coverage",
            "fix": "Add an ERROR HANDLING section for common failure modes",
        })

    # No quality gate / verification
    quality_keywords = ["verify", "check", "validate", "quality", "review", "audit", "pass"]
    has_quality = any(kw in body_lower for kw in quality_keywords)
    if not has_quality:
        issues.append({
            "severity": "medium",
            "issue": "No quality gate or self-verification step",
            "fix": "Add a verification checklist before final output",
        })

    # Sections with very little content (compressed)
    for sec in sections:
        if sec["word_count"] < 20 and sec["title"] not in ("", "Quick Reference"):
            issues.append({
                "severity": "medium",
                "issue": f'Section "{sec["title"]}" is very thin ({sec["word_count"]} words) — likely over-compressed',
                "fix": f'Expand "{sec["title"]}" with concrete instructions, examples, or rules',
            })

    # No examples
    example_keywords = ["example", "before:", "after:", "e.g.", "for instance", "sample"]
    has_examples = any(kw in body_lower for kw in example_keywords)
    if not has_examples:
        issues.append({
            "severity": "low",
            "issue": "No examples in skill body",
            "fix": "Add at least one before/after example or sample output",
        })

    return issues


def analyze_skill(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    sections = extract_sections(body)

    total_words = len(text.split())
    total_lines = len(text.splitlines())
    issues = detect_issues(meta, body, sections)

    return {
        "file": str(path),
        "name": meta.get("name", "unknown"),
        "version": meta.get("version", "unversioned"),
        "description": meta.get("description", ""),
        "description_length": len(meta.get("description", "")),
        "total_words": total_words,
        "total_lines": total_lines,
        "section_count": len(sections),
        "sections": [
            {
                "title": s["title"],
                "level": s["level"],
                "word_count": s["word_count"],
                "subsection_count": len(s.get("subsections", [])),
            }
            for s in sections
        ],
        "issues": issues,
        "issue_count": len(issues),
        "meta": meta,
    }


def print_analysis(result: dict):
    print(f"\n{'═' * 60}")
    print(f"  SKILL ANALYSIS: {result['name']} v{result['version']}")
    print(f"  File: {result['file']}")
    print(f"{'═' * 60}")
    print(f"  Words: {result['total_words']:,} | Lines: {result['total_lines']:,} | Sections: {result['section_count']}")
    print(f"  Description: {result['description_length']} chars")

    print(f"\n  SECTIONS:")
    for sec in result["sections"]:
        indent = "  " if sec["level"] == 2 else "    "
        print(f"  {indent}{'##' if sec['level'] == 2 else '###'} {sec['title']:<40} {sec['word_count']:>5} words")

    if result["issues"]:
        print(f"\n  ISSUES DETECTED ({result['issue_count']}):")
        for issue in sorted(result["issues"], key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["severity"]]):
            icon = "✗" if issue["severity"] == "high" else "⚠" if issue["severity"] == "medium" else "○"
            print(f"\n  {icon} [{issue['severity'].upper()}] {issue['issue']}")
            print(f"      Fix: {issue['fix']}")
    else:
        print(f"\n  ✓ No structural issues detected.")

    print(f"\n{'═' * 60}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python skill_parser.py <SKILL.md> [--json|--sections]")
        sys.exit(1)

    filepath = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "--report"

    result = analyze_skill(filepath)

    if mode == "--json":
        print(json.dumps(result, indent=2))
    elif mode == "--sections":
        for sec in result["sections"]:
            print(f"{'  ' * (sec['level'] - 1)}{'#' * sec['level']} {sec['title']} ({sec['word_count']} words)")
    else:
        print_analysis(result)
