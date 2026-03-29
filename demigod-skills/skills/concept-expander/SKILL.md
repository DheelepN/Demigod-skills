---
name: concept-expander
version: 1.0.0
description: |
  Expands a rough book seed (1 paragraph, bullet points, or a vague idea) into a full,
  structured concept document that the book-writer skill can consume directly. Use when
  the user says "I have an idea for a book," "here's a rough concept," or provides a
  seed that is too thin to drive the full writing workflow. Outputs a ready-to-use
  concept document. Do NOT use for books where a full concept already exists.
allowed-tools:
  - Read
  - Write
  - Bash
---

# Concept Expander

## Scripts

**Validate concept document completeness** before passing to book-writer:
```bash
python scripts/validate_concept.py <concept.md>
python scripts/validate_concept.py <concept.md> --strict   # stricter word count minimums
python scripts/validate_concept.py <concept.md> --json     # machine-readable
```
Checks all required fields (logline, core question, reader, promise, unique angle,
central tension, emotional arc, thematic clusters, genre) and scores completeness.
Also validates the logline for banned words and word count.

**Always run validation before handing the concept document to book-writer.**
A concept that fails validation will produce a weaker structure in Module 2.

You take a rough seed — a paragraph, a title, a feeling, a few bullet points — and develop
it into a complete concept document that drives the entire book-writing workflow.

---

## TRIGGER

Activate when the user provides:
- A vague book idea ("I want to write a book about identity")
- A single title or working title only
- A rough paragraph summary
- A list of themes with no structure
- Anything too thin for book-writer Phase 1 to work with

---

## PROCESS

### Step 1 — Seed Extraction
Read the user's raw input. Identify:
- The core emotional or intellectual question at the heart of the idea
- Who this is likely for (implied audience)
- What genre it maps to in Vivid's categories (Philosophy/Essay, Self-help/Motivational, Non-fiction/Technical)
- Any natural tension or paradox in the idea (this is the engine of good books)

### Step 2 — Clarifying Questions (if needed)
If the seed is genuinely too sparse (under 3 usable signals), ask ONE round of targeted questions:

```
Before I expand this, a few quick questions:
1. Who is this book for — what is their core pain or question?
2. What do you want them to feel or understand by the last page that they don't feel now?
3. Is there a personal story or experience at the root of this idea?
4. Any books that exist in the same space that this should be different from?
```

Do not ask all four if some are already answerable from the seed.

### Step 3 — Concept Document Generation
Produce the full concept document in this format:

---

```
BOOK CONCEPT DOCUMENT
═══════════════════════════════════════════════════════

WORKING TITLE: [compelling title + optional subtitle]
ALTERNATE TITLES: [2 other options]

LOGLINE (one sentence):
[The book's entire premise in 25 words or fewer. If you can't say it in one sentence,
the concept isn't tight enough yet.]

THE CORE QUESTION:
[The one question the book answers. Not a topic — a question. E.g., not "loneliness"
but "Why does being surrounded by people sometimes feel lonelier than being truly alone?"]

THE READER:
Who they are: [demographic + psychographic sketch]
What they're feeling right now: [their current emotional state]
What they've already tried: [what hasn't worked for them]
What they secretly want: [the real desire beneath the surface problem]

THE PROMISE:
[What the reader will have — know, feel, be able to do — after finishing this book
that they don't have now. Be specific. Not "a better life" but exactly what changes.]

GENRE: [Vivid's category]
TONE: [e.g., raw/confessional, philosophical, instructional-personal, polemical]
REGISTER: [e.g., intimate/direct, authoritative/grounded, exploratory/questioning]

THE UNIQUE ANGLE:
[What makes this book different from existing books on this topic. What does Vivid's
lived experience add that a generic author couldn't? Be specific.]

THE CENTRAL TENSION OR PARADOX:
[Every great book has a tension at its core. E.g., "The more you chase connection,
the more alone you feel." Name the paradox this book lives in.]

EMOTIONAL ARC (reader's journey):
Start: [where the reader is emotionally when they open page 1]
Middle: [what they confront, what gets harder before it gets better]
End: [what shifts — not necessarily solved, but transformed]

THEMATIC CLUSTERS (7–10 themes/territories to explore):
1. [Theme + one sentence on what to explore within it]
2.
3.
4.
5.
6.
7.
[add more as needed]

SIGNATURE ELEMENTS:
[Recurring devices, structural choices, or content features that will define this book.
E.g., "dual My Story / My Reflection structure," "opens each chapter with a paradox,"
"uses no external citations — all insight is arrived at through lived experience"]

COMPARABLE BOOKS (comp titles):
[2–3 books this sits near in a bookstore — and crucially, how this is different from each]

ESTIMATED SCOPE:
[short / medium / full-length — with reasoning]

POTENTIAL CHAPTER TERRITORIES (rough, pre-structure):
[8–14 possible chapter-level questions or themes — these feed Phase 2 of book-writer]

RISKS / BLIND SPOTS:
[Honest assessment: what could make this book fall flat? What would a skeptical reader
push back on? What does the author need to be careful not to oversimplify?]

═══════════════════════════════════════════════════════
```

---

## OUTPUT

Deliver the complete concept document.
Then add one line:

```
→ This concept document is ready for the book-writer skill. Upload it or paste it to begin.
```

---

## QUALITY CHECKS

Before delivering, verify:
- [ ] Logline is under 25 words and doesn't use vague terms ("journey," "transformation," "discover")
- [ ] Core question is a genuine question, not a topic
- [ ] The unique angle names something specific Vivid brings — not generic
- [ ] Thematic clusters are distinct from each other (no overlap)
- [ ] The emotional arc has a real middle — not just start and end
- [ ] Comparable books are real, named, and the differentiators are honest
