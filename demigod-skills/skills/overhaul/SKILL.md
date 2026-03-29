---
name: overhaul
version: 1.0.0
description: |
  Upgrades any existing skill file from its current version to a dramatically better one.
  Two modes: AUTOMATED (diagnoses and upgrades everything independently, no user input needed)
  and PERSONALIZED (user-guided — user decides what to upgrade, how deep, what to keep,
  what to add). Triggers when user says "upgrade this skill," "improve this skill,"
  "make this skill better," "overhaul this skill," "v2 this skill," "what's wrong with
  this skill," or uploads a SKILL.md and asks for improvements. Produces a versioned
  upgrade with full changelog. Results should be astonishing — not incremental edits
  but dimensional upgrades.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Overhaul

## Scripts

**Skill parser** — always run first before diagnosing:
```bash
python scripts/skill_parser.py <SKILL.md>
python scripts/skill_parser.py <SKILL.md> --sections    # section structure only
python scripts/skill_parser.py <SKILL.md> --json        # machine-readable
```
Extracts version, sections, word counts, and auto-detects structural issues.
Run this before the 6-module diagnostic — it surfaces obvious problems instantly.

**Version bumper** — run after writing the upgrade:
```bash
python scripts/version_bump.py <SKILL.md>              # auto bump patch
python scripts/version_bump.py <SKILL.md> --minor      # bump minor
python scripts/version_bump.py <SKILL.md> --major      # bump major
python scripts/version_bump.py <SKILL.md> --set 2.0.0  # set specific
python scripts/version_bump.py <SKILL.md> --dry-run    # preview only
```

**Changelog generator** — run after upgrade to document changes:
```bash
python scripts/changelog_gen.py <old_SKILL.md> <new_SKILL.md>
python scripts/changelog_gen.py <old_SKILL.md> <new_SKILL.md> --markdown
python scripts/changelog_gen.py <old_SKILL.md> <new_SKILL.md> --json
```

## References

`references/upgrade_checklist.md` — Pre-delivery checklist and common missing dimensions.
Read when: preparing final delivery, unsure if upgrade is complete enough.
dimensions the original didn't know it needed. Then rebuilding with those gaps filled.

The benchmark for a successful upgrade: the output should feel like a different
generation of the skill, not a cleaner version of the same one.

---

## FIRST STEP — ALWAYS

Read the skill file completely before doing anything else.
Do not begin diagnosis until you have read every line.
Do not begin writing until diagnosis is complete.

---

## MODE SELECTION

After reading the skill, ask the user:

```
I've read [skill name] v[X]. Before I begin, which upgrade mode do you want?

AUTOMATED — I diagnose everything, identify all upgrade vectors, and rebuild
the skill completely on my own. No input needed from you until the final
upgrade is delivered. Best for: skills that need a full generational upgrade.

PERSONALIZED — We go through the diagnosis together. You decide what to upgrade,
how deep to go, what to keep exactly as-is, and you can add your own inputs,
context, or requirements at each stage. Best for: skills where you have specific
opinions about what needs changing.

Which mode?
```

Wait for answer. Then proceed to the correct mode below.

---
---

# AUTOMATED MODE

No user input after mode selection until final delivery.
Run all six diagnostic modules, synthesize findings, rebuild, deliver.

---

## AUTOMATED PHASE 1 — FULL DIAGNOSIS

Run all six modules in sequence. Do not skip any.

---

### DIAGNOSTIC MODULE 1 — INTENT RECONSTRUCTION

Identify:
- **Stated intent**: What does the skill say it does? (frontmatter description + first section)
- **Actual behavior**: What does the skill body actually instruct? (read the full instructions)
- **Gap**: Where does the actual behavior fall short of, diverge from, or contradict stated intent?

The gap between stated intent and actual behavior is always the first upgrade vector.

Document findings:
```
INTENT RECONSTRUCTION
─────────────────────────────────────────────────────
Stated intent:  [what the skill claims to do]
Actual behavior:[what it actually instructs]
Gap identified: [specific divergence — this becomes Upgrade Vector 1]
```

---

### DIAGNOSTIC MODULE 2 — CONFLICT DETECTION

Read the skill looking specifically for internal contradictions:
- Instructions in section A that cancel out instructions in section B
- Rules that would produce opposite behaviors depending on read order
- Trigger conditions that overlap or exclude each other incorrectly
- Output formats defined in multiple places with inconsistencies
- Permissions or constraints that fight each other

Real example from practice: A humanizer skill that strips "negative parallelisms"
would destroy an author's protected signature constructions. The rule and the
exception were never reconciled — conflict invisible until examined under pressure.

Document findings:
```
CONFLICT DETECTION
─────────────────────────────────────────────────────
Conflict 1: [Section X says Y. Section Z says the opposite.]
            Impact: [what breaks when this fires]
Conflict 2: [...]
None found: [if clean]
```

---

### DIAGNOSTIC MODULE 3 — COMPRESSION AUDIT

Find content that has been compressed too thin — important logic buried in one vague
line that deserves its own section, rule, or process.

Signs of over-compression:
- A single bullet that's doing the work of an entire module
- A vague directive like "apply judgment" with no criteria for what good judgment is
- An output format described in 2 lines that should be a full template
- An edge case mentioned in passing with no handling instructions
- A quality standard implied but never defined ("produce high-quality output")
- A multi-step process collapsed into a single instruction

For each compressed item, note:
- What it currently says (the compressed version)
- What it should be expanded into (the full version needed)

Document findings:
```
COMPRESSION AUDIT
─────────────────────────────────────────────────────
Compressed item 1: "[current compressed text]"
Should expand to:  [description of full module/section needed]

Compressed item 2: [...]
```

---

### DIAGNOSTIC MODULE 4 — MISSING DIMENSION SCAN

This is the hardest and most valuable module. Identify what the skill doesn't address
at all — not things it does poorly, but entire categories of problem it has no answer for.

Missing dimensions are invisible in the current skill because they were never thought of.
They only appear when you ask: "What will inevitably happen when this skill is used in
the real world that the current instructions don't cover?"

Check for missing dimensions across these categories:

**Edge case coverage:**
- What happens when the input is ambiguous?
- What happens when the input is too thin to work with?
- What happens when the input is in an unexpected format?
- What happens when the user skips a required step?
- What happens when the output of one module fails before the next module runs?

**Quality definition:**
- Is "good output" defined precisely enough to be reproducible?
- Are there quality gates — checkpoints that must pass before proceeding?
- Is there a self-audit step where the skill verifies its own output?
- Is there a failure mode with a recovery path?

**Protection logic:**
- Are there things the skill should explicitly NOT change or remove?
- Are there user-specific inputs that must be preserved?
- Are there constructions that look like problems but are actually intentional?

**Integration awareness:**
- Should this skill know about other skills it will work alongside?
- Are there external systems, formats, or standards it should reference?
- Does it produce output that another skill will consume — and if so, is the
  output format optimized for that consumption?

**Output consistency:**
- Is the output format defined as a template, or just described loosely?
- Would two runs on the same input produce structurally identical outputs?
- Is versioning handled — does the upgrade produce a versioned output with changelog?

Document findings:
```
MISSING DIMENSION SCAN
─────────────────────────────────────────────────────
Missing dimension 1: [category — what entire handling is absent]
Real-world scenario: [when this would fire and what would go wrong]
Solution:            [what module/section/rule needs to be added]

Missing dimension 2: [...]
```

---

### DIAGNOSTIC MODULE 5 — INTEGRATION ANALYSIS

Examine whether the skill is aware of its ecosystem:

- **Companion skills**: Are there other installed skills this one should reference,
  hand off to, or receive input from? Is the handoff protocol defined?
- **Embedded knowledge**: Is there external domain knowledge this skill should have
  permanently embedded instead of relying on general training?
- **Output consumers**: Does another skill or process consume this skill's output?
  Is the output format optimized for that consumer?
- **Input producers**: Does another skill produce this skill's input? Is the input
  format expected by this skill compatible with what the producer generates?
- **Triggering accuracy**: Does the frontmatter description reliably fire when it
  should? Does it fire when it shouldn't? Is it too broad or too narrow?

Document findings:
```
INTEGRATION ANALYSIS
─────────────────────────────────────────────────────
Companion skill gaps: [skills it should know about but doesn't]
Embedded knowledge gaps: [domain knowledge that should be baked in]
Triggering issues: [description too broad / too narrow / ambiguous]
Output compatibility: [issues with downstream consumers]
```

---

### DIAGNOSTIC MODULE 6 — OUTPUT STANDARD CHECK

Evaluate the precision of the skill's output definition:

- Is the output format defined as a concrete template or just described loosely?
- Is quality defined with measurable or observable criteria?
- Is there a versioning convention — does upgraded output carry a version number?
- Is there a changelog or diff produced alongside the output?
- Is there a self-verification step before final delivery?
- Would someone reading only the output know exactly what skill produced it?

Document findings:
```
OUTPUT STANDARD CHECK
─────────────────────────────────────────────────────
Format definition:    [template / described loosely / missing]
Quality criteria:     [defined / implied / absent]
Versioning:           [present / absent]
Self-verification:    [present / absent]
Consistency:          [would produce same structure every run? Y/N]
```

---

## AUTOMATED PHASE 2 — UPGRADE SYNTHESIS

After all six modules, synthesize findings into an upgrade plan:

```
UPGRADE SYNTHESIS — [Skill Name]
═══════════════════════════════════════════════════════

Current version: [X]
Upgrade target:  [X+1]

UPGRADE VECTORS (ordered by impact — highest first):
1. [Vector from Intent Gap / Conflict / Compression / Missing Dimension / Integration / Output]
   Type: [Intent Gap / Conflict / Compression / Missing Dimension / Integration / Output]
   Current state: [what exists now]
   Upgraded state: [what will exist after]
   Impact: [why this matters — what breaks or fails without it]

2. [...]

WHAT WILL NOT CHANGE:
[List sections, rules, or constructions that are working well and will be preserved exactly]

ESTIMATED SCOPE:
[Minor upgrade (1–3 vectors) / Major upgrade (4–6 vectors) / Generational upgrade (all six)]
```

Then proceed directly to Phase 3. Do not wait for approval in Automated Mode.

---

## AUTOMATED PHASE 3 — FULL REBUILD

Write the complete upgraded skill from scratch.

Do not patch the old skill. Rebuild it entirely using the diagnosis as the foundation.
The old skill is a reference — not the base.

### Rebuild Standards

**Version bump**: Increment version number in frontmatter. If no version exists, add `version: 2.0.0`.

**Description upgrade**: Rewrite the frontmatter description using findings from Module 5
(Integration Analysis). It must:
- Accurately describe what the upgraded skill does (not the old one)
- Include specific trigger phrases — both what the user says AND what context suggests
- Be "pushy" enough to fire reliably — err toward over-triggering rather than under
- Be under 60 words

**Body structure**: Organize around modules, not paragraphs. Every distinct behavior
gets its own named section. Every process gets numbered steps. Every output gets a template.

**Quality gates**: Every module that produces output must have a verification check
before it hands off to the next module.

**Edge case coverage**: Every missing dimension identified in Module 4 gets a dedicated
handling section.

**Protected constructions**: Every conflict identified in Module 2 gets an explicit
protection rule that comes BEFORE the general rules.

**Compression resolution**: Every compressed item from Module 3 gets fully expanded
into its own section.

**Output template**: The final output format is defined as a concrete, reusable template —
not described loosely.

---

## AUTOMATED PHASE 4 — DELIVERY

Deliver in this order:

**1. Diagnostic Report** (brief — the key findings only, not the full internal workings)
```
DIAGNOSTIC REPORT — [Skill Name] v[old] → v[new]
═══════════════════════════════════════════════════════
Vectors addressed: [N]
Type of upgrade: [Minor / Major / Generational]

KEY FINDINGS:
• [Most important finding]
• [Second most important]
• [Third]
[Max 5 bullets — most impactful only]
```

**2. Changelog**
```
CHANGELOG — v[old] → v[new]
═══════════════════════════════════════════════════════
ADDED:
• [New section / module / rule — one line each]

EXPANDED:
• [Previously compressed item → what it became]

FIXED:
• [Conflict resolved]

RESTRUCTURED:
• [Major organizational change]

PRESERVED:
• [What was kept exactly as-is and why]
```

**3. The upgraded SKILL.md** — complete, ready to install

---
---

# PERSONALIZED MODE

User-guided. Every phase has a decision point. User controls depth, scope, and direction.

---

## PERSONALIZED PHASE 1 — DIAGNOSTIC REPORT (SHARED)

Run all six diagnostic modules (same as Automated Mode).
But instead of proceeding directly to rebuild, present findings to the user.

```
DIAGNOSTIC REPORT — [Skill Name] v[X]
═══════════════════════════════════════════════════════

I've analyzed the skill across 6 dimensions. Here's what I found:

─────────────────────────────────────────────────────
1. INTENT GAP
[What the skill claims to do vs. what it actually instructs]
Severity: [Low / Medium / High / Critical]

─────────────────────────────────────────────────────
2. CONFLICTS DETECTED
[List each conflict with impact]
Severity: [Low / Medium / High / Critical]
— or — No conflicts found.

─────────────────────────────────────────────────────
3. OVER-COMPRESSED SECTIONS
[List each compressed item]
Severity: [Low / Medium / High / Critical]
— or — No compression issues found.

─────────────────────────────────────────────────────
4. MISSING DIMENSIONS
[List each missing category with the real-world scenario it breaks]
Severity: [Low / Medium / High / Critical]
— or — No missing dimensions found.

─────────────────────────────────────────────────────
5. INTEGRATION GAPS
[Companion skills it should know about, triggering issues, output compatibility]
Severity: [Low / Medium / High / Critical]
— or — Integration looks solid.

─────────────────────────────────────────────────────
6. OUTPUT STANDARD
[Format precision, quality definition, versioning, self-verification]
Severity: [Low / Medium / High / Critical]
— or — Output standard is well-defined.

═══════════════════════════════════════════════════════
Total upgrade vectors identified: [N]
Estimated upgrade scope: [Minor / Major / Generational]
```

---

## PERSONALIZED PHASE 2 — USER DECISION POINT 1: SCOPE

After the diagnostic report, ask:

```
Before I start upgrading, a few decisions:

1. WHICH FINDINGS do you want to address?
   [List each finding with its severity]
   You can say: "all of them," "only the Critical and High ones,"
   "skip #3 and #5," or name specific ones.

2. DEPTH — for each finding you want addressed, how deep?
   LIGHT   — fix the problem cleanly, minimum new content
   FULL    — expand completely, add all necessary structure
   MAXIMUM — treat as a missing module, build it out entirely

3. ANYTHING TO ADD that I didn't find?
   Any requirements, context, or inputs you want built into the upgrade?
   Anything from your own experience using this skill that should be fixed?

4. ANYTHING TO PROTECT?
   Any sections, rules, or constructions you want kept exactly as-is,
   even if my diagnosis flagged them?

Take your time — this shapes everything.
```

Wait for full answer. Confirm scope before proceeding:

```
Confirmed upgrade scope:
• Addressing: [list of findings to fix]
• Depth: [per finding or uniform]
• Additions: [user-specified additions]
• Protected: [locked sections]

Proceeding to upgrade. I'll check in with you at key decision points.
```

---

## PERSONALIZED PHASE 3 — ITERATIVE BUILD

Build the upgrade section by section, checking in at each major module.

For each major module being added or rebuilt:

```
[MODULE NAME] — Draft

[Show the drafted module]

─────────────────────────────────────────────────────
Does this capture what you wanted?
Options:
→ Approve — move to next module
→ Adjust — tell me what to change
→ Expand — go deeper on [specific part]
→ Simplify — strip back to essentials
→ Replace — I'll rewrite it with your direction
```

Wait for response. Apply changes immediately. Move to next module only on approval.

Key checkpoints (always stop and show):
- After the frontmatter / description rewrite
- After the first major structural module
- After any module that adds entirely new content not in the original
- Before the final assembly

---

## PERSONALIZED PHASE 4 — USER DECISION POINT 2: FINAL REVIEW

Before assembling the final file, present a summary:

```
UPGRADE SUMMARY — Before Final Assembly
═══════════════════════════════════════════════════════

MODULES COMPLETED:
[List each module with approval status]

CHANGES FROM ORIGINAL:
Added:      [N new sections/modules]
Expanded:   [N compressed items]
Fixed:      [N conflicts]
Protected:  [N sections unchanged]
User additions: [N custom inputs incorporated]

FINAL CHECKS:
□ Version number updated?
□ Frontmatter description reflects new capabilities?
□ All approved modules present?
□ Protected sections unchanged?

Ready to assemble. Any last changes before I generate the final file?
```

Wait for confirmation or final adjustments.

---

## PERSONALIZED PHASE 5 — DELIVERY

Same delivery format as Automated Mode:

**1. Changelog** (user-facing — what changed, what was user-directed)
**2. The upgraded SKILL.md** — complete, ready to install

Add a user-input acknowledgment section to the changelog:

```
USER-DIRECTED ADDITIONS:
• [Each user-specified addition or adjustment — credited explicitly]
```

---
---

# SHARED REBUILD STANDARDS (both modes)

These apply regardless of mode. Non-negotiable in every upgrade.

---

## VERSIONING CONVENTION

Always increment version on upgrade:
- Patch (0.0.X): Typo fixes, minor clarifications, no behavior change
- Minor (0.X.0): New sections, expanded content, edge cases added
- Major (X.0.0): Generational rebuild, new modules, structural overhaul

If no version exists in the original: assign `version: 2.0.0` (assumes there was a v1).

---

## FRONTMATTER DESCRIPTION RULES

The description is the triggering mechanism — it determines whether the skill fires.
Every upgrade must include a rewritten description that:

1. States what the skill does (not what it is)
2. States specifically when to use it — include example trigger phrases
3. States what it does NOT handle (prevents false triggers)
4. Is "pushy" — errs toward firing when relevant rather than waiting
5. Is under 60 words
6. Reflects the upgraded capability — not the old one

---

## STRUCTURE STANDARDS

Every upgraded skill must have:

**Named modules** — every distinct behavior gets a named `## SECTION` heading
**Numbered steps** — every process is numbered, not bulleted
**Output templates** — every output is a concrete template, not a description
**Quality gates** — every multi-step module has a verification checkpoint
**Error handling** — every module has at least one "what to do if this fails" rule
**Protected constructions** — any conflict has an explicit protection rule before the general rule
**Edge case handlers** — every identified missing dimension has a dedicated section

---

## QUALITY GATES

Before delivering any upgraded skill in either mode:

- [ ] Version number bumped
- [ ] Frontmatter description rewritten and accurate
- [ ] All diagnostic findings addressed (or explicitly skipped in Personalized)
- [ ] No internal conflicts remain
- [ ] Every compressed item expanded
- [ ] Every missing dimension has a handler
- [ ] Output format is a concrete template
- [ ] Changelog is complete and accurate
- [ ] The upgraded skill would produce astonishing results compared to the original

That last check is the standard. If the upgrade is incremental — if it just cleans up
what was already there without adding new dimensions — it hasn't passed. Go back and
find the missing dimension that was overlooked.

---
---

# WHAT MAKES AN UPGRADE ASTONISHING

The difference between a good upgrade and an astonishing one:

**Good upgrade**: Fixes what's wrong. Cleans up what's messy. Makes existing behavior reliable.

**Astonishing upgrade**: Adds what was never there. Finds the dimension the original
author didn't know to think about. Produces output that makes the user feel the original
skill was a prototype.

The diagnostic module that produces this is **Module 4 — Missing Dimension Scan**.
The most valuable thing you can do in any upgrade is find the category of problem the
skill has no answer for — and build the answer.

In practice this looks like:
- The humanizer that didn't know it needed a DNA protection layer
- The chapter writer that didn't define what "pass" means before humanizing
- The research aggregator that didn't distinguish between direct citations and scaffolding
- The TOC builder that didn't define what "approved" means before writing starts

None of these were visible as problems in the original skills. They only appeared when
you asked: "What will inevitably go wrong when this fires in the real world?"

That question is the engine of astonishing upgrades. Ask it for every module.
Ask it for the skill as a whole. Ask it one more time before delivery.

---
---

# QUICK REFERENCE

```
MODE SELECTION
  → AUTOMATED:    Read → Diagnose (6 modules) → Synthesize → Rebuild → Deliver
  → PERSONALIZED: Read → Diagnose → Show report → User scopes → Build iteratively
                  → User approves each module → Final review → Deliver

6 DIAGNOSTIC MODULES
  1. Intent Reconstruction   — stated vs. actual behavior gap
  2. Conflict Detection      — internal contradictions
  3. Compression Audit       — logic buried too thin
  4. Missing Dimension Scan  — entire categories not addressed (highest value)
  5. Integration Analysis    — ecosystem awareness, triggering accuracy
  6. Output Standard Check   — format precision, quality definition

UPGRADE SEVERITY
  Minor:       1–2 vectors, patch or minor version bump
  Major:       3–4 vectors, minor version bump
  Generational: 5–6 vectors, major version bump

THE TEST
  Would someone who used the original skill feel this is a
  different generation — not just a cleaner version?
  If no → find the missing dimension and add it.
```
