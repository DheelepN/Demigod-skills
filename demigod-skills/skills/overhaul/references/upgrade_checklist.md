# Overhaul — Upgrade Quality Checklist

Run this checklist before delivering any upgraded skill. Every item must pass.

---

## PRE-DELIVERY CHECKLIST

### Frontmatter
- [ ] Version number bumped (patch for minor fixes, minor for new sections, major for rebuild)
- [ ] Description rewritten to reflect upgraded capabilities — not the old skill's description
- [ ] Description includes at least 3 specific trigger phrases
- [ ] Description is under 300 characters
- [ ] Description is "pushy" — errs toward triggering rather than waiting

### Structure
- [ ] Every distinct behavior has a named `## SECTION` heading
- [ ] Every multi-step process is numbered (not bulleted)
- [ ] Every output has a concrete template (not just described)
- [ ] Every module has a quality gate or verification checkpoint
- [ ] Every identified conflict has an explicit protection rule BEFORE the general rule
- [ ] Every missing dimension from Module 4 has a dedicated handler section

### Content
- [ ] All conflicts identified in Module 2 are resolved
- [ ] All compressed items from Module 3 are fully expanded
- [ ] All missing dimensions from Module 4 have handlers
- [ ] Integration gaps from Module 5 are addressed
- [ ] Output format is a concrete template

### The Final Test
- [ ] Would someone who used the original skill feel this is a **different generation** — not just a cleaner version?

If the answer to the final test is NO → go back and find the missing dimension that was overlooked.

---

## VERSION BUMP GUIDE

| Change Type | Version Bump | Example |
|---|---|---|
| Typo fix, minor wording | Patch (0.0.X) | 1.0.0 → 1.0.1 |
| New section, expanded content, edge cases | Minor (0.X.0) | 1.0.0 → 1.1.0 |
| Generational rebuild, new modules, overhaul | Major (X.0.0) | 1.0.0 → 2.0.0 |
| No version in original | Assign 2.0.0 | — → 2.0.0 |

---

## UPGRADE SEVERITY GUIDE

| Vectors Found | Severity | Expected Version Bump |
|---|---|---|
| 1–2 vectors | Minor upgrade | Minor (0.X.0) |
| 3–4 vectors | Major upgrade | Major (X.0.0) |
| 5–6 vectors | Generational | Major (X.0.0) |

---

## THE 6 DIAGNOSTIC MODULES — QUICK REFERENCE

| Module | What It Finds | Why It Matters |
|---|---|---|
| 1. Intent Reconstruction | Gap between stated and actual behavior | First upgrade vector |
| 2. Conflict Detection | Instructions that cancel each other | Silent failures at runtime |
| 3. Compression Audit | Logic buried too thin in one line | Missing handling |
| 4. Missing Dimension Scan | Categories not addressed at all | The highest-value module |
| 5. Integration Analysis | Ecosystem awareness, triggering accuracy | Skills that never fire |
| 6. Output Standard Check | Format precision, quality definition | Inconsistent output |

---

## COMMON MISSING DIMENSIONS (found repeatedly across skills)

These are frequently missing — check for them in every upgrade:

1. **What happens when input is too thin?** (Most skills have no "seed too vague" handler)
2. **What happens when a required step is skipped?** (Most pipelines assume linear execution)
3. **Is there a quality gate before the final output?** (Most skills just output without self-checking)
4. **Are protected constructions defined?** (Skills that strip content often destroy intentional choices)
5. **Is the output format a template or just described?** (Described outputs are inconsistent across runs)
6. **What is the recovery path when a module fails?** (Most skills have no error → retry path)
