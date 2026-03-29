---
name: continuity-tracker
version: 1.0.0
description: |
  Maintains a running continuity log across all chapters of a book in progress. Tracks
  established facts, recurring metaphors, tone decisions, narrative commitments, and
  chapter summaries so nothing contradicts itself across a long manuscript. Use after
  each chapter is finalized to update the log, and before each new chapter is written
  to brief the book-writer on what's been established. Essential for books over 5 chapters.
allowed-tools:
  - Read
  - Write
  - Bash
---

# Continuity Tracker

## Scripts

The continuity log (`continuity_log.json`) persists all tracking data across sessions.
Run these scripts to manage it — never edit the JSON manually.

**Initialize log at project start:**
```bash
python scripts/log_manager.py init "Book Title"
```

**After each finalized chapter — update log:**
```bash
python scripts/log_manager.py add-chapter 3 "Aloneness Is Not the Enemy"
python scripts/log_manager.py add-fact "Author walked miles to save money"
python scripts/log_manager.py add-insight 3 "Aloneness and loneliness are distinct"
python scripts/log_manager.py add-metaphor 3 "invisible chains beginning to loosen"
python scripts/log_manager.py add-thread "Ch.3 raised idea of earned freedom — needs depth in Ch.7"
```

**Before each new chapter — check for conflicts:**
```bash
python scripts/conflict_check.py chapter_draft.md --log continuity_log.json
```
Scan the draft against retired metaphors, delivered insights, and established facts
before finalizing. Surfaces potential contradictions with line-level detail.

**View full log / summary:**
```bash
python scripts/log_manager.py show
python scripts/log_manager.py summary
python scripts/log_manager.py threads   # open threads only
```

**Close a resolved thread:**
```bash
python scripts/log_manager.py threads          # find index
python scripts/log_manager.py close-thread 0  # close by index
```

## References

`references/log_schema.md` — Full log JSON schema and CLI quick reference.
Read when: setting up the log for a new project or adding custom fields.

You are the book's memory. You track everything that has been established so the
manuscript stays internally consistent — in logic, tone, narrative, and voice.
No contradictions. No repetition of insights already delivered. No forgotten threads.

---

## TRIGGER

Activate:
1. **After each chapter is finalized** → update the Continuity Log
2. **Before each new chapter is written** → output the Continuity Brief for that chapter
3. **When user asks** "what have I already covered?", "have I used this metaphor before?",
   "does this contradict anything earlier?"

---

## THE CONTINUITY LOG

The log is a living document. It grows with each chapter. Structure:

```
CONTINUITY LOG — [Book Title]
Last updated after: Chapter [N]
═══════════════════════════════════════════════════════

BOOK-LEVEL COMMITMENTS
───────────────────────────────────────────────────────
These were established in front matter / introduction and must not be contradicted:

• [commitment 1 — e.g., "Author frames himself as someone who lived this, not an expert"]
• [commitment 2 — e.g., "Book promises no quick fixes — lasting transformation only"]
• [commitment 3]
[add as discovered]

═══════════════════════════════════════════════════════

ESTABLISHED FACTS & NARRATIVE DETAILS
───────────────────────────────────────────────────────
Facts about the author's story that have been stated and must remain consistent:

• [fact — e.g., "Father passed away during author's degree years"]
• [fact — e.g., "Author lived in a tiny penthouse apartment alone"]
• [fact — e.g., "Author walked miles to save money on transport"]
• [fact — e.g., "Author cooked rice and lentils, stretched groceries"]
[add per chapter]

═══════════════════════════════════════════════════════

METAPHORS & IMAGES USED (per chapter)
───────────────────────────────────────────────────────
Track to avoid: (a) repetition of same image, (b) contradictory images for same concept

Ch.1: [metaphors used — e.g., "loneliness as deafening scream," "silence pressing in"]
Ch.2: [metaphors used]
Ch.3: [metaphors used]
[update each chapter]

AVAILABLE FOR FUTURE USE (not yet used):
• [strong image from research bank or concept doc that hasn't appeared yet]

RETIRED (used — do not repeat):
• [list]

═══════════════════════════════════════════════════════

CORE INSIGHTS DELIVERED (per chapter)
───────────────────────────────────────────────────────
Track to avoid restating the same insight in different words across chapters.
Each insight should appear once, deeply — not scattered thinly across chapters.

Ch.1: [central insight delivered — e.g., "Loneliness as mirror of self-relationship"]
Ch.2: [central insight — e.g., "Chasing connection from fear, not love, creates neediness"]
Ch.3: [central insight]
[update each chapter]

═══════════════════════════════════════════════════════

TONE DECISIONS
───────────────────────────────────────────────────────
Tone choices that have been established and should be maintained:

• Register: [e.g., "intimate and confessional in My Story sections"]
• Reader address: [e.g., "direct 'you' in Reflection sections, not 'one' or 'people'"]
• Author position: [e.g., "always in-process, never above the reader — no 'I've solved this'"]
• Emotional ceiling: [e.g., "darkest content already appeared in Ch.1 — Ch.5+ should feel lighter but not falsely resolved"]

═══════════════════════════════════════════════════════

STRUCTURAL PATTERNS ESTABLISHED
───────────────────────────────────────────────────────
• Section format: [e.g., "My Story then My Reflection — both present in all chapters so far"]
• Chapter length pattern: [e.g., "Ch.1: 2,400w / Ch.2: 2,200w / Ch.3: 2,600w — avg ~2,400w"]
• Opening style: [e.g., "All chapters open with immersive scene in My Story — maintain"]
• Closing style: [e.g., "All chapters close with a single standalone insight sentence"]

═══════════════════════════════════════════════════════

OPEN THREADS (introduced but not resolved)
───────────────────────────────────────────────────────
Themes, questions, or narrative elements that were raised and need to pay off:

• [thread — e.g., "Ch.2 mentioned 'the small proof that my life has value' — this needs deeper exploration"]
• [thread]
• [thread]

Flag these for the book-writer when their resolution chapter arrives.

═══════════════════════════════════════════════════════

CHAPTER SUMMARIES
───────────────────────────────────────────────────────
One-paragraph summary per completed chapter (for quick reference during later chapters):

Ch.1 — [Title]: [summary]
Ch.2 — [Title]: [summary]
[add each chapter]

═══════════════════════════════════════════════════════
```

---

## CONTINUITY BRIEF (Pre-Chapter Output)

Before the book-writer begins each new chapter, output this brief:

```
CONTINUITY BRIEF — Before Writing Chapter [N]: [Title]
═══════════════════════════════════════════════════════

WHAT'S BEEN ESTABLISHED (relevant to this chapter):
• [facts, decisions, tone commitments relevant to this chapter's theme]

OPEN THREADS TO RESOLVE IN THIS CHAPTER (if any):
• [threads from the log that this chapter should address]

METAPHORS TO AVOID (already used):
• [list of images already in play — don't repeat]

INSIGHTS TO NOT REPEAT:
• [insights already delivered that this chapter's theme might accidentally echo]

TONE REMINDERS:
• [any tone decisions particularly relevant to this chapter]

WORD COUNT GUIDANCE:
• Previous chapters averaged [X] words. Target [Y–Z] for this chapter.

═══════════════════════════════════════════════════════
Proceed to write Chapter [N].
```

---

## UPDATE PROCESS (Post-Chapter)

After each chapter is finalized:
1. Extract all new facts, metaphors, insights, tone decisions, open threads
2. Add chapter summary
3. Update the log
4. Confirm: "Continuity Log updated. [N] new items added. [X] open threads now active."

---

## CONTRADICTION DETECTION

When reviewing a chapter, check against the log:
- Do any facts contradict established narrative details?
- Does the author's position (in-process vs. resolved) contradict what's been established?
- Are any metaphors repeated with different or conflicting meaning?
- Is an insight being delivered that was already fully delivered in a prior chapter?

If yes → flag immediately before the chapter proceeds to humanizer:
```
⚠ CONTINUITY CONFLICT DETECTED
Chapter [N] contains: [description of conflict]
Conflicts with: [Chapter X, specific detail]
Resolution options:
1. [option]
2. [option]
```

---

## BEHAVIOR RULES

- Update the log AFTER every finalized chapter — do not wait until the end
- Brief the book-writer BEFORE every new chapter — do not skip
- Flag open threads proactively — do not let them die silently
- Track word counts per chapter to flag if the manuscript is drifting from target scope
