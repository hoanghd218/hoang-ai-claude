---
name: mkt-book-to-wisdom-posts
description: "Extract wisdom from books and create viral Facebook wisdom posts in Vietnamese. Supports 6 proven formats: Progressive Reduction, Never Too Late List, Contrast Pairs, Numbered Skills List, Intangible Assets, Bold Statement. Input is a book name, book excerpt, knowledge passage, or topic. Output is 2-3 ready-to-post Facebook posts with caption + image text. USE WHEN user says 'tạo bài từ sách', 'book to post', 'bóc kiến thức từ sách', 'wisdom post', 'tạo content từ sách', 'bài viết từ sách', 'extract book wisdom', 'sách ra content', 'tạo post triết lý', 'content sách', 'viết bài từ kiến thức sách'."
---

# Book to Wisdom Posts

Extract wisdom from books and create high-engagement Facebook posts using 6 proven viral formats.

## Input Types

| Input | How to handle |
|-------|---------------|
| **Book name only** | Use known knowledge about the book to extract key lessons |
| **Book excerpt/passage** | Extract wisdom directly from the provided text |
| **Topic + book** | Focus extraction on the specific topic within the book |
| **Raw knowledge/quote** | Transform directly into post formats |

If the book is unfamiliar and no excerpt is provided, ask user for key passages or a summary.

## Workflow

### Step 1: Extract Wisdom Points

Read the input and extract 5-10 key wisdom points. Each point should be:
- A standalone insight (understandable without context)
- Actionable or deeply resonant
- Expressible in 2-8 words (for image text)

Categorize each point:
- **Habit/Discipline** → Progressive Reduction, Numbered List
- **Mindset/Growth** → Never Too Late, Intangible Assets
- **Balance/Boundary** → Contrast Pairs
- **Principle/Rule** → Numbered List, Bold Statement
- **Self-worth/Character** → Intangible Assets, Never Too Late
- **Counter-intuitive** → Bold Statement, Contrast Pairs

### Step 2: Select Formats

Load [references/post_formats.md](references/post_formats.md) for detailed format structures and examples.

Choose 2-3 formats that best match the extracted wisdom. Prioritize variety — never repeat the same format.

**Format selection guide:**

| Book content type | Best formats |
|---|---|
| Habits, discipline, consistency | Progressive Reduction, Numbered List |
| Mindset, growth, resilience | Never Too Late, Intangible Assets |
| Balance, boundaries, relationships | Contrast Pairs |
| Principles, rules, skills | Numbered List, Bold Statement |
| Self-worth, character, inner wealth | Intangible Assets, Never Too Late |
| Counter-intuitive ideas | Bold Statement, Contrast Pairs |

### Step 3: Generate Posts

For each selected format, generate:

1. **Caption** (1-2 sentences): Short, profound, creates curiosity. No hashtags, no emojis.
2. **Image text**: Structured content following the exact format template from references.

**Writing rules:**
- Vietnamese, conversational tone
- No emojis or special characters in image text
- Items: short phrases (2-8 words), not paragraphs
- Bold headline for the image
- Signature: `@tranvanhoang.com`
- Stay faithful to the book's actual teachings — do not invent or distort

### Step 4: Output

```
═══════════════════════════════════════
📚 NGUỒN: [Tên sách / Tác giả]
🎯 CHỦ ĐỀ: [Topic extracted]
═══════════════════════════════════════

📝 Wisdom Points:
1. [Point 1]
2. [Point 2]
...

═══════════════════════════════════════
POST #1 — Format: [Tên format]
═══════════════════════════════════════

📌 Caption:
[Caption text — copy-paste ready]

🖼️ Image Text:
[Full image content — copy-paste ready for design]

---

═══════════════════════════════════════
POST #2 — Format: [Tên format]
═══════════════════════════════════════

📌 Caption:
[Caption text]

🖼️ Image Text:
[Full image content]

---

(POST #3 nếu có)
```

Save output to `workspace/content/facebook/` if user requests.
Filename: `[book-slug]-wisdom-posts.md`

## Integration

After generating posts, suggest user run `mkt-create-actionable-post-image` skill to render image text into actual Facebook post images (supports list, contrast, comparison templates).

## Quality Criteria

- Each post is independently shareable — no need for the book
- Wisdom feels universal, not book-specific jargon
- Caption creates a "gap" that makes reader want to see the image
- Image text is scannable in under 10 seconds
- Posts feel like wisdom, not book summaries

## References

- [references/post_formats.md](references/post_formats.md) — 6 format templates with examples and selection guide. **Load before Step 2.**
