#!/usr/bin/env python3
"""
log_manager.py — Read, write, and update the continuity log

The continuity log is stored as a JSON file alongside the manuscript.
This script manages all log operations: init, update, read, and summary.

Usage:
    python log_manager.py init <book_title> [--log log.json]
    python log_manager.py show [--log log.json]
    python log_manager.py summary [--log log.json]
    python log_manager.py add-chapter <N> <title> [--log log.json]
    python log_manager.py add-fact <fact> [--log log.json]
    python log_manager.py add-insight <chapter_n> <insight> [--log log.json]
    python log_manager.py add-metaphor <chapter_n> <metaphor> [--log log.json]
    python log_manager.py add-thread <thread> [--log log.json]
    python log_manager.py close-thread <thread_index> [--log log.json]
    python log_manager.py threads [--log log.json]
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

DEFAULT_LOG = "continuity_log.json"


def load_log(log_path: str) -> dict:
    path = Path(log_path)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def save_log(log: dict, log_path: str):
    Path(log_path).write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


def init_log(book_title: str, log_path: str) -> dict:
    log = {
        "book_title": book_title,
        "created": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "last_chapter": 0,
        "commitments": [],
        "established_facts": [],
        "metaphors": {
            "by_chapter": {},
            "available": [],
            "retired": [],
        },
        "insights": {},
        "tone_decisions": {
            "register": "",
            "reader_address": "",
            "author_position": "",
            "emotional_ceiling": "",
        },
        "structural_patterns": {
            "section_format": "",
            "avg_chapter_words": 0,
            "opening_style": "",
            "closing_style": "",
            "chapter_word_counts": [],
        },
        "open_threads": [],
        "closed_threads": [],
        "chapter_summaries": {},
    }
    save_log(log, log_path)
    print(f"  ✓ Log initialized: {log_path}")
    print(f"    Book: {book_title}")
    return log


def show_log(log: dict):
    print(f"\n{'═' * 60}")
    print(f"  CONTINUITY LOG — {log['book_title']}")
    print(f"  Last updated after Chapter {log['last_chapter']}")
    print(f"{'═' * 60}")

    if log["commitments"]:
        print(f"\n  BOOK-LEVEL COMMITMENTS ({len(log['commitments'])}):")
        for c in log["commitments"]:
            print(f"    • {c}")

    if log["established_facts"]:
        print(f"\n  ESTABLISHED FACTS ({len(log['established_facts'])}):")
        for f in log["established_facts"]:
            print(f"    • {f}")

    if log["metaphors"]["by_chapter"]:
        print(f"\n  METAPHORS USED:")
        for ch, mets in sorted(log["metaphors"]["by_chapter"].items(), key=lambda x: int(x[0])):
            print(f"    Ch.{ch}: {', '.join(mets)}")
        if log["metaphors"]["retired"]:
            print(f"    Retired: {', '.join(log['metaphors']['retired'])}")

    if log["insights"]:
        print(f"\n  INSIGHTS DELIVERED:")
        for ch, insight in sorted(log["insights"].items(), key=lambda x: int(x[0])):
            print(f"    Ch.{ch}: {insight}")

    open_threads = [t for t in log["open_threads"] if not t.get("closed")]
    if open_threads:
        print(f"\n  OPEN THREADS ({len(open_threads)}):")
        for i, t in enumerate(open_threads):
            print(f"    [{i}] {t['thread']}")
            if t.get("introduced_in"):
                print(f"         Introduced: Ch.{t['introduced_in']}")

    if log["chapter_summaries"]:
        print(f"\n  CHAPTER SUMMARIES ({len(log['chapter_summaries'])}):")
        for ch, summary in sorted(log["chapter_summaries"].items(), key=lambda x: int(x[0])):
            title = summary.get("title", f"Chapter {ch}")
            text = summary.get("summary", "")[:80]
            print(f"    Ch.{ch} — {title}: {text}...")

    print(f"\n{'═' * 60}\n")


def summary_log(log: dict):
    open_threads = [t for t in log["open_threads"] if not t.get("closed")]
    print(f"\n  {log['book_title']} — Continuity Summary")
    print(f"  Chapters completed: {log['last_chapter']}")
    print(f"  Facts established:  {len(log['established_facts'])}")
    print(f"  Insights delivered: {len(log['insights'])}")
    print(f"  Open threads:       {len(open_threads)}")
    if open_threads:
        print(f"  ⚠ Unresolved threads:")
        for t in open_threads:
            print(f"    · {t['thread'][:60]}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=[
        "init", "show", "summary", "add-chapter", "add-fact",
        "add-insight", "add-metaphor", "add-thread", "close-thread", "threads"
    ])
    parser.add_argument("args", nargs="*")
    parser.add_argument("--log", default=DEFAULT_LOG)
    parsed = parser.parse_args()

    log_path = parsed.log
    cmd = parsed.command
    args = parsed.args

    if cmd == "init":
        title = " ".join(args) if args else "Untitled"
        init_log(title, log_path)

    elif cmd in ("show",):
        log = load_log(log_path)
        if not log:
            print(f"  No log found at {log_path}. Run: python log_manager.py init <title>")
            sys.exit(1)
        show_log(log)

    elif cmd == "summary":
        log = load_log(log_path)
        if not log:
            print(f"  No log found at {log_path}")
            sys.exit(1)
        summary_log(log)

    elif cmd == "add-chapter":
        log = load_log(log_path)
        if not log:
            print("  No log found. Run init first.")
            sys.exit(1)
        n = int(args[0]) if args else log["last_chapter"] + 1
        title = " ".join(args[1:]) if len(args) > 1 else f"Chapter {n}"
        log["last_chapter"] = n
        log["last_updated"] = datetime.now().isoformat()
        if str(n) not in log["chapter_summaries"]:
            log["chapter_summaries"][str(n)] = {"title": title, "summary": ""}
        save_log(log, log_path)
        print(f"  ✓ Chapter {n}: {title} added to log")

    elif cmd == "add-fact":
        log = load_log(log_path)
        if not log:
            sys.exit(1)
        fact = " ".join(args)
        log["established_facts"].append(fact)
        log["last_updated"] = datetime.now().isoformat()
        save_log(log, log_path)
        print(f"  ✓ Fact added: {fact}")

    elif cmd == "add-insight":
        log = load_log(log_path)
        if not log:
            sys.exit(1)
        ch = args[0] if args else str(log["last_chapter"])
        insight = " ".join(args[1:]) if len(args) > 1 else ""
        log["insights"][ch] = insight
        log["last_updated"] = datetime.now().isoformat()
        save_log(log, log_path)
        print(f"  ✓ Insight for Ch.{ch} added")

    elif cmd == "add-metaphor":
        log = load_log(log_path)
        if not log:
            sys.exit(1)
        ch = args[0] if args else str(log["last_chapter"])
        metaphor = " ".join(args[1:]) if len(args) > 1 else ""
        if ch not in log["metaphors"]["by_chapter"]:
            log["metaphors"]["by_chapter"][ch] = []
        log["metaphors"]["by_chapter"][ch].append(metaphor)
        log["metaphors"]["retired"].append(metaphor)
        log["last_updated"] = datetime.now().isoformat()
        save_log(log, log_path)
        print(f"  ✓ Metaphor added to Ch.{ch} and retired")

    elif cmd == "add-thread":
        log = load_log(log_path)
        if not log:
            sys.exit(1)
        thread = " ".join(args)
        log["open_threads"].append({
            "thread": thread,
            "introduced_in": str(log["last_chapter"]),
            "closed": False,
            "added": datetime.now().isoformat(),
        })
        log["last_updated"] = datetime.now().isoformat()
        save_log(log, log_path)
        print(f"  ✓ Thread added: {thread}")

    elif cmd == "close-thread":
        log = load_log(log_path)
        if not log:
            sys.exit(1)
        idx = int(args[0]) if args else -1
        open_threads = [t for t in log["open_threads"] if not t.get("closed")]
        if 0 <= idx < len(open_threads):
            open_threads[idx]["closed"] = True
            open_threads[idx]["closed_in"] = str(log["last_chapter"])
            log["closed_threads"].append(open_threads[idx])
            log["last_updated"] = datetime.now().isoformat()
            save_log(log, log_path)
            print(f"  ✓ Thread [{idx}] closed: {open_threads[idx]['thread'][:60]}")
        else:
            print(f"  ✗ Invalid thread index: {idx}")

    elif cmd == "threads":
        log = load_log(log_path)
        if not log:
            sys.exit(1)
        open_threads = [t for t in log["open_threads"] if not t.get("closed")]
        print(f"\n  Open threads ({len(open_threads)}):\n")
        for i, t in enumerate(open_threads):
            print(f"  [{i}] Introduced Ch.{t.get('introduced_in', '?')}: {t['thread']}")
        print()
