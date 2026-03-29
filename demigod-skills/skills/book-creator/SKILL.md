---
name: book-creator
version: 1.0.0
description: |
  Complete end-to-end book creation system for Vivid (Dheelep N). One skill that does
  everything: concept expansion, research aggregation, structure options, full intake
  questionnaire, table of contents, chapter writing (guided or autonomous), 7-dimension
  chapter audit, DNA-aware humanizer pass, continuity tracking, and KDP-ready DOCX output.
  Triggers when user says "write a book," "start a book," "I have a book idea," "create a
  manuscript," "write chapter," "humanize this," "audit this chapter," or uploads a concept
  document. All scripts and references are bundled — install this one skill and the entire
  pipeline works without installing anything else.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - WebSearch
  - AskUserQuestion
---

# Book Creator — Complete Book Production System for Vivid

One skill. Every tool needed to go from a seed idea to a KDP-ready published manuscript.
No other skills needed. Everything is bundled.

---

## SCRIPTS (all in `scripts/`)

### Pre-writing
```bash
python scripts/validate_concept.py <concept.md>          # validate concept doc completeness
python scripts/validate_concept.py <concept.md> --strict # stricter word count minimums
```

### During writing
```bash
python scripts/word_count.py <manuscript.md>                        # per-chapter word counts
python scripts/word_count.py <manuscript.md> --target medium        # vs KDP targets
python scripts/toc_extract.py <manuscript.md>                       # verify structure
python scripts/toc_extract.py <manuscript.md> --markdown            # markdown TOC output

python scripts/log_manager.py init "Book Title"                     # init continuity log
python scripts/log_manager.py add-chapter 1 "Chapter Title"         # log chapter
python scripts/log_manager.py add-fact "Established fact"           # log narrative fact
python scripts/log_manager.py add-insight 1 "Core insight"          # log delivered insight
python scripts/log_manager.py add-metaphor 1 "metaphor used"        # retire metaphor
python scripts/log_manager.py add-thread "Open thread description"  # track open thread
python scripts/log_manager.py close-thread 0                        # resolve thread
python scripts/log_manager.py show                                   # full log view
python scripts/log_manager.py summary                               # quick status
python scripts/conflict_check.py <chapter.md>                       # check for contradictions
```

### Per-chapter quality
```bash
python scripts/dna_scan.py <chapter.md>                  # identify protected DNA constructions
python scripts/scan_ai_patterns.py <chapter.md>          # flag all 25 AI patterns
python scripts/scan_ai_patterns.py <chapter.md> --summary # quick count view
python scripts/score_report.py --chapter "Title"          # interactive audit scoring
python scripts/score_report.py --chapter "Title" --output audit.md  # save report
```

### Research
```bash
python scripts/bank_formatter.py research_bank.json          # view research bank
python scripts/bank_formatter.py research_bank.json --validate # check quality
```

### Final output
```bash
python scripts/kdp_check.py <manuscript.docx>              # KDP pre-flight check
python scripts/kdp_check.py <manuscript.docx> --trim 6x9   # with trim size
```

---

## REFERENCES (all in `references/`)

- `references/kdp_specs.md` — KDP trim sizes, margins, typography, page count estimates
- `references/patterns_quick_ref.md` — All 25 AI pattern trigger words and before/after fixes
- `references/thinkers_reference.md` — Curated philosophers and quotes for Vivid's genres
- `references/log_schema.md` — Continuity log JSON schema and full CLI reference

Read the relevant reference at the start of each phase:
- Concept phase → thinkers_reference.md
- Writing phase → kdp_specs.md + log_schema.md
- Humanizer phase → patterns_quick_ref.md
- Output phase → kdp_specs.md

---

## PIPELINE MAP

```
INPUT: SEED IDEA / ROUGH CONCEPT / FULL CONCEPT DOCUMENT
              ↓
   ┌─────────────────────────────────┐
   │  PHASE 1: CONCEPT               │ ← skip if full concept doc already provided
   │  Expand seed → concept doc      │
   │  Validate: validate_concept.py  │
   └─────────────────────────────────┘
              ↓
   ┌──────────────────────────────────────┐
   │  PHASE 2: STRUCTURE OPTIONS          │
   │  3 proposals → user picks one        │
   └──────────────────────────────────────┘
              ↓
   ┌───────────────────────────────────────────┐
   │  PHASE 3: INTAKE QUESTIONNAIRE            │
   │  26 questions → all decisions locked      │
   └───────────────────────────────────────────┘
              ↓
   ┌───────────────────────────────────────────────────┐
   │  PHASE 4: RESEARCH BANK                           │
   │  Concept + TOC → quotes, thinkers per chapter     │
   │  Validate: bank_formatter.py --validate           │
   └───────────────────────────────────────────────────┘
              ↓
   ┌─────────────────────────────────────────┐
   │  PHASE 5: TABLE OF CONTENTS             │
   │  Full TOC → user approves               │
   │  Verify: toc_extract.py                 │
   └─────────────────────────────────────────┘
              ↓
   ┌────────────────────────────────────────────────────────────┐
   │  PHASE 6: CHAPTER LOOP  (repeats for every chapter)        │
   │                                                            │
   │  6A. Continuity Brief ←───────────────────────────────┐   │
   │      log_manager.py show + conflict_check.py           │   │
   │        ↓                                               │   │
   │  6B. Chapter Writer (Guided or Autonomous)             │   │
   │        ↓                                               │   │
   │  6C. Chapter Auditor                                   │   │
   │      dna_scan.py → scan_ai_patterns.py → score_report.py   │
   │        ↓ PASS                                          │   │
   │  6D. Humanizer Pass                                    │   │
   │      DNA protection → strip 25 patterns → DNA rewrite  │   │
   │        ↓                                               │   │
   │  6E. Continuity Log Update ────────────────────────────┘   │
   │      log_manager.py + word_count.py                        │
   └────────────────────────────────────────────────────────────┘
              ↓
   ┌──────────────────────────────────────────────────────┐
   │  PHASE 7: KDP DOCX OUTPUT                            │
   │  Format → kdp_check.py → validate → deliver          │
   └──────────────────────────────────────────────────────┘
```

---
---

# PHASE 1 — CONCEPT EXPANDER

## TRIGGER
Activate Phase 1 when the user provides:
- A vague idea, single title, rough paragraph, or loose bullet points
- Anything too thin to build structure options from

If a complete concept document is uploaded → **skip to Phase 2**.
After generating the concept document → run `python scripts/validate_concept.py <file>`.
Do not proceed to Phase 2 if validation scores below 80% or any required field fails.

## PROCESS

### Step 1 — Seed Extraction
Identify:
- Core emotional or intellectual question at the heart of the idea
- Implied audience and their pain
- Genre fit (Philosophy/Essay | Self-help/Motivational | Non-fiction/Technical)
- Natural tension or paradox (this is the engine)

### Step 2 — Clarifying Questions (only if seed has under 3 usable signals)
Ask ONE round, max 4 questions:
```
1. Who is this for — what is their core pain or question?
2. What should they feel or understand by the last page that they don't now?
3. Is there a personal story at the root of this idea?
4. Any existing books in this space that this should be different from?
```

### Step 3 — Concept Document Output

```
BOOK CONCEPT DOCUMENT
═══════════════════════════════════════════════════════

WORKING TITLE: [compelling title + optional subtitle]
ALTERNATE TITLES: [2 other options]

LOGLINE (one sentence, under 25 words):
[Entire premise. Banned words: "journey," "transformation," "discover"]

THE CORE QUESTION:
[A genuine question, not a topic.]

THE READER:
  Who they are:             [demographic + psychographic]
  What they feel right now: [current emotional state]
  What they've tried:       [what hasn't worked]
  What they secretly want:  [real desire beneath surface problem]

THE PROMISE:
[Specific — what they'll have after finishing. Not "a better life."]

GENRE:    [Vivid's category]
TONE:     [raw/confessional | philosophical | instructional-personal]
REGISTER: [intimate/direct | authoritative/grounded | exploratory]

THE UNIQUE ANGLE:
[What Vivid's lived experience adds that a generic author couldn't.]

THE CENTRAL TENSION OR PARADOX:
[The paradox the book lives in.]

EMOTIONAL ARC:
  Start:  [reader's emotional state on page 1]
  Middle: [what they confront — harder before better]
  End:    [what shifts — not solved, but transformed]

THEMATIC CLUSTERS (7–10):
  1. [Theme + one sentence on territory]
  2–10. [...]

SIGNATURE ELEMENTS:
[Recurring devices or structural choices.]

COMPARABLE BOOKS:
[2–3 real comp titles + how this is different from each]

ESTIMATED SCOPE: [short / medium / full-length]

POTENTIAL CHAPTER TERRITORIES (8–14):
[Possible chapter-level questions or themes]

RISKS / BLIND SPOTS:
[What could make this fall flat?]

═══════════════════════════════════════════════════════
```

### Quality Checks
- [ ] Logline under 25 words, no banned terms
- [ ] Core question is a genuine question, not a topic
- [ ] Unique angle is specific to Vivid's lived experience
- [ ] Thematic clusters are distinct
- [ ] Emotional arc has a real, difficult middle
- [ ] `validate_concept.py` scores ≥ 80%

→ Proceed to Phase 2.

---
---

# PHASE 2 — STRUCTURE OPTIONS

Present 3 structure options. User picks one.

```
STRUCTURE OPTIONS
═══════════════════════════════════════════════════════

OPTION A — [Name, e.g., "Focused & Tight"]
Parts: [N] | Chapters: [N] | ~[X]–[Y]k words | ~[Z] pages
Logic: [why this fits the concept]
Chapter sketch:
  Introduction: [title]
  Ch.1: [title] | Ch.2: [title] | ...

OPTION B — [Name]
[same format]

OPTION C — [Name]
[same format]

═══════════════════════════════════════════════════════
Which structure resonates? You can mix elements.
```

Wait for user choice. Confirm hybrid if mixing.
→ Proceed to Phase 3.

---
---

# PHASE 3 — INTAKE QUESTIONNAIRE

Lock all 26 decisions. Ask all at once. Use defaults for skipped answers, flag them.

```
BOOK INTAKE QUESTIONNAIRE
═══════════════════════════════════════════════════════

A. FORMATTING & PUBLISHING
 1. Trim size: 5×8 / 6×9 / 8.5×11 / other?
 2. Font preference: [default: Georgia 11pt]
 3. Line spacing: 1.15 / 1.5 / double?
 4. Chapter titles: numbers only / names only / both?
 5. Part dividers? Yes / No
 6. Headers: book title left + chapter title right? Or other?
 7. Page numbers: bottom center / bottom outside / top outside?

B. VISUAL ELEMENTS
 8. Text-only or images? → If images: AI prompts / supply files? → Color or B&W?
 9. Chapter opener decoration? Yes / No / Specify
10. Pull quotes or callout boxes? Yes / No

C. FRONT & BACK MATTER
11. Foreword or Preface? I draft / You write / Skip
12. Dedication? Yes (text?) / No
13. "How to Use This Book" section? Yes / No
14. About the Author: existing bio / write new / skip
15. "Stay in Touch" page? Yes / No
16. Acknowledgments? Yes / No

D. CHAPTER STRUCTURE
17. "My Story + My Reflection" dual-section format? Yes / No / Modified
18. For technical books: exercises, code blocks, case studies? Yes / No
19. Reflection questions at chapter end? Yes / No
20. Epigraph per chapter? Yes / No

E. WRITING MODE
21. GUIDED (you provide notes per chapter) or AUTONOMOUS (I write from concept alone)?

F. VOICE & CONTENT
22. Personal stories to include? [list or upload]
23. Topics OFF LIMITS?
24. Desired total length? [or defer to structure]
25. Author name on cover? [real / pen name / confirm "Dheelep N"]
26. Specific quotes or thinkers to include or avoid?

═══════════════════════════════════════════════════════
```

Confirm: "All inputs locked. Building Research Bank and TOC."
→ Proceed to Phase 4.

---
---

# PHASE 4 — RESEARCH AGGREGATOR

Build the Research Bank. Save as `research_bank.json`.
Validate after building: `python scripts/bank_formatter.py research_bank.json --validate`
Fix any flagged issues before proceeding.

Read `references/thinkers_reference.md` before selecting any sources.

## Research categories per chapter

**A. Philosophical Anchors** (max 1 per chapter appears in final text)
Format: `[Thinker/Work] — [Core idea] — [Chapter connection]`

Priority thinkers for Vivid's genres:
- Solitude / inner life: Rilke, Thoreau, Pascal, Kierkegaard, Montaigne
- Philosophy of identity: Epictetus, Marcus Aurelius, Sartre, Camus, Beauvoir
- Psychology of self: Viktor Frankl, Carl Rogers, Nathaniel Branden
- Eastern frameworks: Stoic practice, non-attachment, witness consciousness
- Modern psychology: attachment theory, self-determination theory, ACT

**B. Empirical Anchors** (1–2 per chapter max)
Format: `[Finding in plain English] — [Source] — [Application]`

**C. Quotes** (under 30 words, not overexposed)
Format: `"[Quote]" — [Author, Work]`

**D. Conceptual Oppositions**
Best argument against the chapter's central claim.

## Research Bank output format

```
RESEARCH BANK — [Book Title]
═══════════════════════════════════════════════════════

GLOBAL ANCHORS:
[3–5 ideas thematic to the whole manuscript]

CHAPTER [N]: [Title]
─────────────────────────────────────
Theme: [one sentence]
Philosophical anchors: [items]
Quotes: ["quote" — Author]
Research: [finding + source]
Opposition: [counterargument]
Writing notes: [how to deploy in Vivid's style]
═══════════════════════════════════════════════════════
```

→ Proceed to Phase 5.

---
---

# PHASE 5 — TABLE OF CONTENTS

Build full TOC. Verify with `python scripts/toc_extract.py <manuscript.md>` after writing begins.
Do NOT start writing until TOC is explicitly approved.

```
TABLE OF CONTENTS — [Book Title]
═══════════════════════════════════════════════════════

FRONT MATTER
  Half-title | Title | Copyright | Dedication | How to Use | TOC

BODY
  Introduction: [Title]
  PART I: [Title]
    Chapter 1: [Title]
    Chapter 2: [Title]
  ...

BACK MATTER
  Epilogue | About the Author | Stay in Touch | Acknowledgments

─────────────────────────────────────────────────────
Estimated: ~[X]k words / ~[Y] pages at [trim size]
═══════════════════════════════════════════════════════
```

→ Proceed to Phase 6 loop.

---
---

# PHASE 6 — CHAPTER LOOP

Run all 5 sub-phases for every chapter. Loop until all chapters complete.

---

## PHASE 6A — CONTINUITY BRIEF

**Initialize log on Chapter 1:**
```bash
python scripts/log_manager.py init "Book Title"
```

**Before every chapter — run:**
```bash
python scripts/log_manager.py show
python scripts/conflict_check.py <previous_chapter.md>
```

Output the brief:

```
CONTINUITY BRIEF — Before Writing Chapter [N]: [Title]
═══════════════════════════════════════════════════════
ESTABLISHED (relevant to this chapter):
• [facts, tone decisions, commitments]

OPEN THREADS TO RESOLVE HERE:
• [threads needing payoff]

METAPHORS TO AVOID (retired):
• [list]

INSIGHTS NOT TO REPEAT:
• [already delivered]

TONE REMINDERS:
• [chapter-specific considerations]

WORD COUNT GUIDANCE:
• Prior avg: [X] words. Target [Y–Z] for this chapter.
═══════════════════════════════════════════════════════
```

---

## PHASE 6B — CHAPTER WRITER

### GUIDED MODE
1. Present chapter title + 2–3 sentence writing brief
2. Ask: "What key points, stories, or insights should I include?"
3. Wait for input → write using inputs + Style DNA below

### AUTONOMOUS MODE
Write without waiting. Use concept doc, Research Bank, TOC, questionnaire answers, Style DNA, Continuity Brief.
Checkpoint every 2–3 chapters: "Chapters [X–Y] complete. Any direction changes?"

### Chapter length targets
| Scope | Words per chapter |
|---|---|
| Short (under 20k total) | 1,500–2,000 |
| Medium (20–50k) | 2,000–3,500 |
| Full-length (50k+) | 3,500–5,000 |

### Default structure (self-help / philosophy)

**My Story** — raw first-person narrative. Past tense. Immersive. Confessional. No hedging.

**My Reflection and Insights** — philosophical synthesis. Present tense. Oscillates I/you.
Moves from personal pain outward to universal truth.

### Pain-to-Transformation Arc (every chapter, no exceptions)
```
1. ENTER THE PAIN       — at least 2–3 paragraphs. don't rush.
2. WRONG ATTEMPTS       — show the failing strategies. readers recognize themselves here.
3. THE REALIZATION      — arrives from inside the experience, not external advice.
4. THE SHIFT            — perspective change, not a tidy fix.
5. THE LANDING          — one sentence that reframes everything. does not summarize.
```

### Opening rule
NEVER open with: definition / "In today's world" / statistics paragraph
DO open with: scene / confession / question that makes the reader stop

### Closing rule
End on a single reframe — not a summary. The closing line should feel earned.

---

## PHASE 6B-DNA — VIVID'S WRITING STYLE DNA
*Extracted from Master of Being Alone by Dheelep N*

### Voice — Raw, Personal, Never Preachy
- Leads with vulnerability. Arrives at insight through pain, not theory.
- Never announces wisdom. Lets experience speak.
- Addresses reader directly: "you," "my friend," rhetorical questions.
- Honest about failure, ambiguity, not-yet-knowing.
- Always in-process — never above the reader.

Sample: *"I won't sugarcoat it. The path to mastering solitude is not a gentle stroll through a sunlit meadow."*

### Sentence Rhythm
- Short punchy sentences land the blow: "It didn't work." / "I failed every time."
- Long sentences build emotional complexity then release.
- Semicolons used naturally for rhythm.
- Rhetorical questions as pivots, not decoration.
- No 2+ consecutive sentences of the same structure.

### Paragraph Density
- 3–7 sentences per paragraph. Never a wall of text.
- Each paragraph has one central beat.
- No filler. No restatement.

### Metaphors & Imagery
- Physical, grounded, sensory. Maps emotional states to physical sensations.
- Protected examples: "knife that cut me deeper every day" / "beggar asking for scraps of attention" / "invisible chains beginning to loosen" / "silence pressed in like a physical weight"
- Never recycle: journey, storm, turning point, crossroads, chapter of life

### Philosophical Integration
- Philosophy is embodied, not academic.
- Arrives at conclusions through experience, then names them simply.
- Uses paradox: "The more independent you become, the more connected you feel."
- Max 1 external citation per chapter.

### Signature Phrases (use sparingly, never formulaically)
- "But here's..." — pivot to deeper truth
- "The hardest part wasn't..." — reframe of the obvious
- "Not [surface X], but [deeper Y]"
- "That is what [X] did to me from the inside."
- Direct reader address mid-paragraph: "...and you start to see."
- Single standalone closing sentence that reframes everything

### Vocabulary Register
- Accessible but emotionally elevated.
- Protected elevated words: "insidious," "imperceptibly," "agonizing," "desolate," "conspicuously," "grotesque," "suffocating," "unraveling"
- Avoids jargon, buzzwords, self-help clichés, passive voice.

### Chapter Titles
Short. Direct. Declarative or interrogative. The title is a promise.
Examples: "Why It Hurts So Much" / "Stop Chasing Connection" / "Aloneness Is Not the Enemy"

### Hard Anti-Patterns (never write these)
- Generic motivational fluff: "you've got this," "believe in yourself"
- Academic distance: "it can be argued that," "research suggests"
- Bullet-point wisdom inside narrative sections
- Rushed resolution (pain → fix in under 3 paragraphs)
- More than 1 external quote per chapter
- Any sentence that could appear on LinkedIn
- Arriving at conclusions too cleanly

### Genre adjustments

**Philosophy / Essay**
- Chapters can be shorter (1,500–2,500w) and denser
- "My Story" optional — pure essay acceptable on some chapters
- Tone: contemplative, probing, occasionally unsettling

**Self-Help / Motivational**
- Always use My Story + My Reflection structure
- Personal anecdotes are the engine — never strip for general advice
- Avoid: 3-step formulas, numbered tips in narrative, toxic positivity

**Non-Fiction / Technical**
- Structure: The Problem → The Concept → How It Works → In Practice
- Vivid's voice still applies: open with real scenario, not a definition
- Tone: clear, direct, grounded — never textbook flat

---

## PHASE 6C — CHAPTER AUDITOR

Run after every chapter draft. Scripts first, then qualitative audit.

**Run scripts:**
```bash
python scripts/dna_scan.py <chapter_file>          # identify protected constructions
python scripts/scan_ai_patterns.py <chapter_file>  # flag AI patterns
python scripts/score_report.py --chapter "Title"   # generate scored report
```

**Score 7 dimensions (1–5 each):**

| Dimension | What to check |
|---|---|
| Voice Authenticity | Opens with scene/confession, immersive My Story, no LinkedIn sentences |
| Pain-to-Transformation Arc | Pain entered fully, wrong attempts shown, realization from within, perspective shift |
| Sentence Rhythm | Varied length, short punchy sentences, rhetorical questions as pivots |
| Metaphor & Imagery | Physical/grounded, specific, no recycled images, min 2 strong images |
| Structural Integrity | Sections demarcated, one beat per paragraph, within word count |
| AI Pattern Contamination | Clean of all 25 patterns (5=clean, 1=heavy) |
| Reader Resonance | Specific pain named, "how did he know" moment, author in-process |

**Audit report format:**
```
CHAPTER AUDIT — [Title]
Words: [X] / Target: [Y]
═══════════════════════════════════════════════════════
Voice Authenticity          [X/5]
Pain-to-Transformation Arc  [X/5]
Sentence Rhythm             [X/5]
Metaphor & Imagery          [X/5]
Structural Integrity        [X/5]
AI Pattern Contamination    [X/5]
Reader Resonance            [X/5]
───────────────────────────────────
OVERALL                     [X/35]
VERDICT: PASS / CONDITIONAL PASS / REVISE

REQUIRED FIXES (≤3): [specific line callouts + fix direction]
RECOMMENDED (4): [optional]
STRONGEST MOMENTS: [2–3 lines to protect]
═══════════════════════════════════════════════════════
```

**Verdicts:**
- 28–35 → PASS → proceed to 6D
- 21–27 → CONDITIONAL PASS → proceed to 6D, fix after
- Under 21 → REVISE → back to 6B with fix list

---

## PHASE 6D — HUMANIZER PASS

Only runs on PASS or CONDITIONAL PASS. Never on REVISE.

**Always run scripts first:**
```bash
python scripts/dna_scan.py <chapter_file>         # Step 1 — find protected constructions
python scripts/scan_ai_patterns.py <chapter_file> # Step 2 — find AI patterns to eliminate
```

Read `references/patterns_quick_ref.md` for the full trigger word list.

### Step 1 — DNA Protection

Tag all protected constructions BEFORE eliminating anything.

| Protected | Rule |
|---|---|
| Negative parallelisms: "Not the silence, but what it forced me to face" | Grounded in specific experience → protect |
| Parallel peaks: "The freedom to love... The freedom to walk..." | Earned accumulation → protect |
| Weighted em dashes around emotional phrases | "That thought — that single image —" → protect |
| Signature phrases | "But here's..." / "The hardest part wasn't..." → always protect |
| Elevated vocabulary naming felt experience | "insidious," "agonizing," "suffocating" → protect |
| Physical imagery: "pressed down on my chest" | Specific + grounded → protect |

### Step 2 — Eliminate AI Patterns (25 patterns — unprotected text only)

**Content:** Significance inflation · Notability claims · Superficial -ing endings · Promotional language · Vague attributions · Challenges/Future sections

**Language:** AI vocabulary (delve, tapestry, nuanced, embark, realm, foster, transformative, impactful, robust, unpack, holistic, synergy, leverage, navigate-as-metaphor) · Copula avoidance (serves as → is) · Negative parallelisms (generic) · Rule of three (generic) · Synonym cycling · False ranges

**Style:** Em dash overuse (generic connectors) · Boldface overuse · Inline-header lists · Title case headings · Emojis · Curly quotes

**Communication:** Chatbot artifacts (I hope this helps, let me know, of course!) · Knowledge-cutoff disclaimers · Sycophantic tone

**Filler:** Filler phrases (in order to, due to the fact that, at this point in time, it is important to note, at its core, in today's world, in conclusion) · Hedging overload · Generic positive conclusions · Hyphen overuse (cross-functional, data-driven, decision-making)

### Step 3 — Vivid Style Rewrite

Actively reshape toward his DNA — not passive editing:

- **Voice check:** Does it sound like confessing or presenting? → Rewrite as confessing.
- **Arc check:** Pain → insight too fast (under 3 paragraphs)? → Insert wrong attempt + cost.
- **Rhythm check:** All sentences same length? → Add one very short sentence after a long accumulation.
- **Imagery check:** Abstract emotional claim with no physical sensation? → Ground it in the body.
- **Opening check:** Does it still drop the reader in cold? → Re-read and verify.
- **Closing check:** Does it reframe or summarize? → Must reframe.

**Six rewrite techniques:**
1. **Confession Opening** — replace general claim with personal scene
2. **Slow the Arc** — insert wrong attempt → why it failed → cost → then insight
3. **Ground the Abstract** — add specific personal detail before the claim + physical image after
4. **Punch Landing** — replace soft ending with one short direct sentence
5. **Reader Address** — shift to "you" for one paragraph in Reflection sections
6. **Reframe Close** — replace summary ending with single sentence that reframes everything

### Step 4 — Self-Audit

Ask: *"What makes this still obviously AI-generated or generic?"*
- [ ] Rhythm too tidy? (even pacing, no variation)
- [ ] Still no opinions — only neutral reporting?
- [ ] Could any section appear in a press release? → rewrite
- [ ] Author above the experience rather than inside it?
- [ ] Any metaphors still recycled?
- [ ] Opening still hooks? Closing still reframes?
- [ ] Does this sound like Vivid — or just "good human writing"?

### Step 5 — Output
1. Draft rewrite (after DNA protection + pattern elimination)
2. Self-audit bullets (what still reads AI or generic)
3. Final version (after style rewrite + self-audit fixes) ← the deliverable
4. Changes summary: Stripped / Protected / Added

---

## PHASE 6E — CONTINUITY LOG UPDATE

After each finalized chapter:

```bash
python scripts/log_manager.py add-chapter [N] "[Title]"
python scripts/log_manager.py add-fact "[new established fact]"
python scripts/log_manager.py add-insight [N] "[core insight delivered]"
python scripts/log_manager.py add-metaphor [N] "[metaphor used — now retired]"
python scripts/log_manager.py add-thread "[any open thread introduced]"
python scripts/word_count.py manuscript.md --target [short|medium|full]
python scripts/log_manager.py summary
```

**Contradiction check before closing:**
```bash
python scripts/conflict_check.py <current_chapter.md>
```

If conflicts detected → surface with resolution options, do NOT auto-resolve.

Confirm: "Log updated after Chapter [N]. [X] items added. [Y] threads open."
→ Loop back to Phase 6A for next chapter.

---
---

# PHASE 7 — KDP DOCX OUTPUT

Run pre-flight check first:
```bash
python scripts/kdp_check.py <manuscript.docx> --trim [5x8|6x9|8.5x11]
```

Read `references/kdp_specs.md` for all trim dimensions, margin requirements,
typography standards, and page count estimates before generating the DOCX.

Use the docx skill at `/mnt/skills/public/docx/SKILL.md` for generation.

## KDP Trim Dimensions (DXA — 1440 DXA = 1 inch)

| Trim | Width | Height | Outside | Inside (gutter) | Top | Bottom |
|---|---|---|---|---|---|---|
| 5×8 | 7,200 | 11,520 | 864 | 1,008 | 1,008 | 864 |
| 6×9 | 8,640 | 12,960 | 864 | 1,080 | 1,080 | 864 |
| 8.5×11 | 12,240 | 15,840 | 1,008 | 1,260 | 1,260 | 1,008 |

## Typography

```javascript
// Body: Georgia 11pt, 1.15 spacing
{ font: "Georgia", size: 22, lineSpacing: { line: 276, lineRule: "auto" } }
// Chapter title: Georgia 18pt bold centered
{ font: "Georgia", size: 36, bold: true, alignment: CENTER, spacing: { before: 720, after: 480 } }
// Section heading: Georgia 14pt bold
{ font: "Georgia", size: 28, bold: true, spacing: { before: 480, after: 240 } }
// Part title: Georgia 20pt bold centered, own page
{ font: "Georgia", size: 40, bold: true, alignment: CENTER, spacing: { before: 2880, after: 2880 } }
```

## Headers & Footers
- Even pages: book title, left-aligned
- Odd pages: chapter title, right-aligned
- Chapter first page: no header
- Page numbers: bottom outside

## Front Matter (in order)
Half-title → Title → Copyright → Dedication → How to Use → TOC → blank if needed

## Chapter Layout
- Each chapter: new page (PageBreak before heading)
- Body: justified, first paragraph no indent, subsequent paragraphs 360 DXA indent
- Section headings: bold, left-aligned, 240 DXA space above

## Validation
```bash
python scripts/office/validate.py manuscript.docx
```
If fails: unpack → fix XML → repack.

---
---

# STYLE OVERRIDE

If user uploads a new sample and says "match this style instead":
1. Read sample (minimum 3,000 words)
2. Extract style DNA using the 13-point framework from Phase 6B-DNA
3. Flag: "Style overridden for this session. Using [book title] as reference."
Vivid's embedded DNA remains the permanent default for new sessions.

---

# ERROR HANDLING

| Situation | Action |
|---|---|
| Concept too vague | Run Phase 1 clarifying questions before proceeding |
| validate_concept.py below 80% | Fix required fields before Phase 2 |
| Skipped questionnaire answers | Use defaults, flag at top of affected chapters |
| Chapter audit REVISE verdict | Return to Phase 6B — do NOT humanize a failing chapter |
| Chapter over/under word count | Flag → ask: expand / trim / proceed as-is |
| conflict_check.py finds conflicts | Surface with resolution options — do NOT auto-resolve |
| kdp_check.py fails | Fix reported issues before delivering |
| User skips a phase | Proceed from current state, flag gap and downstream impact |
| Style override sample under 3,000 words | Ask for more text — sample too short for reliable extraction |

---

# QUICK REFERENCE

```
PHASE 1  Concept Expander      — seed → concept doc → validate_concept.py
PHASE 2  Structure Options     — 3 proposals → user picks
PHASE 3  Intake Questionnaire  — 26 questions → all decisions locked
PHASE 4  Research Aggregator   — concept + TOC → bank → bank_formatter.py --validate
PHASE 5  Table of Contents     — TOC → user approves → toc_extract.py
PHASE 6A Continuity Brief      — log_manager.py show + conflict_check.py
PHASE 6B Chapter Writer        — Guided or Autonomous + Style DNA
PHASE 6C Chapter Auditor       — dna_scan + scan_ai_patterns + score_report
PHASE 6D Humanizer Pass        — protect DNA → strip 25 patterns → rewrite → self-audit
PHASE 6E Log Update            — log_manager + word_count + conflict_check
PHASE 7  KDP DOCX Output       — kdp_check → format → validate → deliver
```
