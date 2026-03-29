---
name: research-aggregator
version: 1.0.0
description: |
  Given a book's concept document and TOC, aggregates relevant quotes, thinkers,
  frameworks, data points, anecdotes, and philosophical references — organized by
  chapter — for use during the writing phase. Use after TOC is approved and before
  chapter writing begins. Produces a Research Bank document the book-writer draws from.
  Do NOT use for fiction books where no external references are needed.
allowed-tools:
  - Read
  - Write
  - Bash
  - WebSearch
---

# Research Aggregator

## Scripts

Save the research bank as `research_bank.json` after building it.

**Validate bank quality** (checks quote lengths, banned sources, missing fields):
```bash
python scripts/bank_formatter.py research_bank.json --validate
```

**View formatted bank:**
```bash
python scripts/bank_formatter.py research_bank.json
python scripts/bank_formatter.py research_bank.json --chapter 3  # single chapter
```

**Export as JSON for pipeline use:**
```bash
python scripts/bank_formatter.py research_bank.json --json
```

## References

`references/thinkers_reference.md` — Curated thinkers, works, and pre-validated quotes
aligned with Vivid's genres (Philosophy/Essay, Self-help, Non-fiction/Technical).
Read when: building philosophical anchors or selecting quotes for any chapter.

**Always read the thinkers reference before selecting sources.**
It includes a banned sources list and overexposed quotes to avoid.

You build the Research Bank — a structured reference document organized by chapter that
the book-writer draws from during writing. Quality over quantity. Every item must earn
its place by being genuinely usable in the writing, not just topically adjacent.

---

## TRIGGER

Activate after Phase 4 (TOC approval) in the book-writing workflow, or when the user says:
- "Find references for my book"
- "Research this topic for my book"
- "Build a research bank for [book title/topic]"

---

## INPUT REQUIRED

1. The approved Table of Contents (chapter titles + structure)
2. The concept document (especially: core question, themes, reader profile)
3. Genre (determines what kind of research is most useful)

---

## RESEARCH CATEGORIES

For each chapter, gather items across these categories (not all are needed for every chapter):

### A. Philosophical / Intellectual Anchors
Thinkers, frameworks, or ideas that resonate with the chapter's theme.
Format: `[Thinker/Work] — [Core idea in 1 sentence] — [How it connects to this chapter]`

Vivid's approach: he arrives at these truths through experience, then names the concept.
So these are NOT citations to use directly — they're conceptual validation. Max 1 per chapter
should appear in the final text. The rest are background scaffolding.

Priority thinkers for Vivid's genres:
- Philosophy of identity: Epictetus, Marcus Aurelius, Simone de Beauvoir, Sartre, Camus
- Solitude / inner life: Rilke, Thoreau, Pascal, Kierkegaard, Montaigne
- Psychology of self: Carl Rogers, Viktor Frankl, Nathaniel Branden
- Eastern frameworks: Stoicism, Advaita Vedanta concepts (non-attachment, witness consciousness)
- Modern psychology: attachment theory, self-determination theory, cognitive defusion (ACT)

### B. Empirical / Research Anchors
Studies, data, or documented findings relevant to the chapter's claims.
Format: `[Finding in plain English] — [Source if known or searchable] — [Chapter application]`

Use sparingly — Vivid is not a data-heavy writer. 1–2 per chapter max.
Prioritize: psychology studies, behavioral research, neuroscience of emotion.

### C. Quotes
Powerful, precise quotes that could open a chapter or punctuate a key insight.
Format: `"[Quote]" — [Author, Work if known]`

Standards for a usable quote:
- Under 30 words
- Not overused (no "Be the change," no "The unexamined life")
- Says something that earns a standalone line
- Vivid would have thought of this himself — the quote confirms, not compensates

### D. Anecdote / Case Study Templates
Brief real-world examples or documented cases that illustrate the chapter's theme.
These are NOT about name-dropping celebrities. Prioritize: ordinary people, historical figures
with specific documented experiences, or well-known stories with fresh angles.

### E. Conceptual Oppositions
The strongest counterargument to the chapter's central claim. Useful for:
- Anticipating reader resistance
- Building nuance into the argument
- Structuring the "wrong attempts" section of the pain-to-transformation arc

---

## OUTPUT FORMAT

Produce one Research Bank document structured like this:

```
RESEARCH BANK — [Book Title]
Generated for: [TOC chapters listed]
═══════════════════════════════════════════════════════

GLOBAL ANCHORS (apply to the whole book, not a single chapter)
───────────────────────────────────────────────────────
[3–5 foundational ideas/thinkers/quotes that are thematic to the entire manuscript]

═══════════════════════════════════════════════════════

CHAPTER 1: [Title]
───────────────────────────────────────────────────────
Theme reminder: [one sentence on what this chapter is about]

Philosophical anchors:
• [item]
• [item]

Quotes:
• "[quote]" — [Author]
• "[quote]" — [Author]

Research/data:
• [finding + source]

Conceptual opposition:
• [The best argument against this chapter's claim]

Writing notes:
[Any specific suggestions for how to deploy this research in Vivid's style —
e.g., "Don't cite Epictetus directly — arrive at his conclusion through the story,
then let the quote confirm it at the end"]

═══════════════════════════════════════════════════════

CHAPTER 2: [Title]
[same structure]

...
═══════════════════════════════════════════════════════

UNUSED BUT NOTABLE
[Interesting material that didn't fit a specific chapter but could be useful]
```

---

## QUALITY FILTERS

Before adding any item to the Research Bank, ask:
1. Would Vivid actually use this? (Does it fit his voice and approach?)
2. Is this specific enough to be useful? (No vague attributions — "researchers say" fails)
3. Does this enrich or just decorate? (Decoration gets cut)
4. Is the quote clean enough to stand alone without explanation?

Remove anything that fails these filters.

---

## VIVID-SPECIFIC RESEARCH RULES

- **No pop-psychology self-help citations** (no Tony Robbins, no Brené Brown framework
  names, no "growth mindset")
- **No overexposed quotes** (Einstein on insanity, Churchill, Mandela patience quote)
- **Prioritize: philosophers who wrote from lived struggle** (Marcus Aurelius in war,
  Frankl in camps, Montaigne in grief)
- **Favor precision over prestige** — a precise quote from an unknown thinker beats a
  famous vague one
- **Eastern philosophy welcome but used lightly** — Vivid's framework is his own; external
  philosophy is seasoning, not the meal
