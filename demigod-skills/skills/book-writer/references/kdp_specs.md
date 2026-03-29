# KDP Publishing Specifications Reference

Complete KDP interior formatting requirements for print-on-demand.

---

## Trim Sizes (DXA units — 1440 DXA = 1 inch)

| Trim     | Width DXA | Height DXA | Common Use |
|----------|-----------|------------|------------|
| 5×8      | 7,200     | 11,520     | Compact non-fiction, poetry |
| 5.5×8.5  | 7,920     | 12,240     | Standard non-fiction |
| 6×9      | 8,640     | 12,960     | Most common for trade paperback |
| 6.14×9.21| 8,842     | 13,262     | Slightly taller trade |
| 7×10     | 10,080    | 14,400     | Workbooks, textbooks |
| 8×10     | 11,520    | 14,400     | Illustrated books |
| 8.5×11   | 12,240    | 15,840     | Workbooks, journals |

---

## Minimum Margins by Page Count

KDP requires larger inside margins as page count increases (to account for binding).

| Page Count | Inside (Gutter) | Outside | Top    | Bottom |
|------------|-----------------|---------|--------|--------|
| 24–150     | 0.375"          | 0.25"   | 0.25"  | 0.25"  |
| 151–300    | 0.5"            | 0.25"   | 0.25"  | 0.25"  |
| 301–500    | 0.625"          | 0.25"   | 0.25"  | 0.25"  |
| 501–700    | 0.75"           | 0.25"   | 0.25"  | 0.25"  |
| 701–828    | 0.875"          | 0.25"   | 0.25"  | 0.25"  |

**Vivid's standard margins (6×9, 200–300 pages):**

| Side    | Inches | DXA   |
|---------|--------|-------|
| Inside  | 0.75"  | 1,080 |
| Outside | 0.6"   | 864   |
| Top     | 0.75"  | 1,080 |
| Bottom  | 0.6"   | 864   |

---

## Typography Standards

| Element          | Font     | Size | Weight | Spacing |
|------------------|----------|------|--------|---------|
| Body text        | Georgia  | 11pt | Normal | 1.15    |
| Chapter title    | Georgia  | 18pt | Bold   | Before: 0.5" After: 0.33" |
| Section heading  | Georgia  | 14pt | Bold   | Before: 0.33" After: 0.17"|
| Part title       | Georgia  | 20pt | Bold   | Centered, full page |
| Epigraph         | Georgia  | 10pt | Italic | Centered, 0.5" margins |
| Footer/Header    | Georgia  | 9pt  | Normal | — |

---

## Body Text Layout

- **Alignment**: Justified
- **First paragraph** after heading: No indent
- **Subsequent paragraphs**: First-line indent 0.25" (360 DXA)
- **Line spacing**: 1.15 (line: 276, lineRule: auto in docx-js)
- **Paragraph spacing**: 0 before, 0 after (spacing handled by line indent)

---

## Headers and Footers

- **Even pages (verso/left)**: Book title, left-aligned
- **Odd pages (recto/right)**: Chapter title, right-aligned
- **Chapter first page**: No header (suppress)
- **Part divider pages**: No header, no footer
- **Page numbers**: Bottom outside (left on even, right on odd)
- **Start page numbering**: From Chapter 1 (front matter uses Roman numerals or no numbers)

---

## Front Matter Order (standard KDP)

1. Half-title page (title only)
2. Also by the author (optional)
3. Title page (title + subtitle + author)
4. Copyright page
5. Dedication
6. Table of Contents
7. Foreword / Preface (if any)
8. Introduction

## Back Matter Order

1. Epilogue / Conclusion
2. Acknowledgments
3. About the Author
4. Also by the Author (optional)
5. Index (non-fiction)
6. Bibliography (academic)

---

## Image Requirements

| Type  | Minimum DPI | Color Mode | Format |
|-------|-------------|------------|--------|
| B&W   | 300 DPI     | Grayscale  | PNG/TIFF |
| Color | 300 DPI     | RGB        | PNG/TIFF |
| Cover | 300 DPI     | RGB        | JPG/TIFF |

---

## File Requirements

- **Format**: DOCX (recommended) or PDF
- **Max file size**: 650 MB
- **Fonts**: Must be embedded or standard system fonts
- **No password protection**
- **No form fields**

---

## Page Count Estimator

At 11pt Georgia, 1.15 spacing, 6×9 with standard margins:
- ~250–280 words per page
- 20,000 words ≈ 75–80 pages
- 40,000 words ≈ 145–160 pages
- 60,000 words ≈ 215–240 pages
- 80,000 words ≈ 290–320 pages

---

## Common KDP Rejection Reasons

1. Margins too small (especially inside/gutter)
2. Images below 300 DPI
3. Fonts not embedded
4. Blank pages at unexpected locations
5. File size over 650 MB
6. Page size doesn't match trim size selected at upload
7. Header/footer content in the margin bleed area
