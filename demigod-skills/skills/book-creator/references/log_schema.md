# Continuity Log — Schema Reference

The continuity log is a JSON file (`continuity_log.json`) maintained
alongside the manuscript. This document describes every field.

---

## Full Schema

```json
{
  "book_title": "string — the book's working title",
  "created": "ISO datetime — when the log was initialized",
  "last_updated": "ISO datetime — last update timestamp",
  "last_chapter": "integer — last chapter number completed",

  "commitments": [
    "string — book-level promises established in front matter/intro"
  ],

  "established_facts": [
    "string — factual details about the author's story, must stay consistent"
  ],

  "metaphors": {
    "by_chapter": {
      "1": ["metaphor used in chapter 1", "another metaphor"],
      "2": ["metaphor used in chapter 2"]
    },
    "available": ["strong images not yet used"],
    "retired": ["all metaphors used — do not repeat"]
  },

  "insights": {
    "1": "Core insight fully delivered in chapter 1",
    "2": "Core insight delivered in chapter 2"
  },

  "tone_decisions": {
    "register": "string — e.g., intimate/confessional in My Story",
    "reader_address": "string — e.g., direct 'you' in Reflection",
    "author_position": "string — e.g., always in-process, never above",
    "emotional_ceiling": "string — e.g., darkest content in Ch.1"
  },

  "structural_patterns": {
    "section_format": "string — e.g., My Story + My Reflection",
    "avg_chapter_words": "integer — running average",
    "opening_style": "string — e.g., immersive scene",
    "closing_style": "string — e.g., single reframe sentence",
    "chapter_word_counts": [2400, 2200, 2600]
  },

  "open_threads": [
    {
      "thread": "string — the thread description",
      "introduced_in": "string — chapter number",
      "closed": false,
      "added": "ISO datetime"
    }
  ],

  "closed_threads": [
    {
      "thread": "string",
      "introduced_in": "string",
      "closed": true,
      "closed_in": "string — chapter where resolved",
      "added": "ISO datetime"
    }
  ],

  "chapter_summaries": {
    "1": {
      "title": "Chapter 1 title",
      "summary": "One-paragraph summary of what was covered"
    }
  }
}
```

---

## Field Guidelines

### `commitments`
Book-level promises that must never be contradicted. Examples:
- "Author frames himself as someone who lived this, not an expert"
- "Book promises no quick fixes — lasting transformation only"
- "Author is always in-process, never looking back from arrival"

### `established_facts`
All narrative details stated in the manuscript that must remain consistent:
- "Father passed away during author's degree years"
- "Lived in a tiny penthouse apartment alone"
- "Walked miles to save money on transport"
- "Cooked rice and lentils, stretched groceries"

### `metaphors.retired`
Once a metaphor is used anywhere in the manuscript, it goes here.
The conflict checker (`conflict_check.py`) scans new chapters against this list.

### `insights`
One core insight per chapter. Track to avoid restating:
- Ch.1: "Loneliness as mirror of self-relationship"
- Ch.2: "Chasing connection from fear, not love, creates neediness"
- Ch.3: "Aloneness and loneliness are different — one is chosen"

### `open_threads`
Thematic or narrative threads introduced that haven't been resolved:
- "Ch.2 mentioned 'the small proof that my life has value' — needs deeper exploration"
- "Ch.3 established reader's 'wrong attempts' pattern — needs to pay off in Ch.7"

---

## CLI Quick Reference

```bash
# Initialize
python log_manager.py init "My Book Title"

# Add chapter
python log_manager.py add-chapter 1 "Why It Hurts So Much"

# Add established fact
python log_manager.py add-fact "Author's father passed during degree years"

# Add insight delivered
python log_manager.py add-insight 1 "Loneliness as mirror of self-relationship"

# Add metaphor (auto-retires it)
python log_manager.py add-metaphor 1 "deafening scream inside my head"

# Add open thread
python log_manager.py add-thread "Ch.2 mentioned small proof of self-value — needs depth"

# Close a thread (by index)
python log_manager.py threads          # list open threads
python log_manager.py close-thread 0  # close thread at index 0

# View full log
python log_manager.py show

# Summary only
python log_manager.py summary

# Conflict check before finalizing a chapter
python conflict_check.py chapter_5.md --log continuity_log.json
```
