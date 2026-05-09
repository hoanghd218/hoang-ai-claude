---
name: image-post-creator
description: "Phân tích nội dung bài viết Facebook, đưa ra prompt tạo ảnh minh họa bằng Nano Banana Pro. Hỗ trợ dạng: các bước, so sánh, ẩn dụ, concept."
version: 5.0.0
---

# Facebook Knowledge Post → Image Creator

Tạo hình ảnh bổ trợ thông tin cho bài Facebook chia sẻ kiến thức. Hình ảnh là dạng typography-based (text-heavy), KHÔNG phải ảnh chụp hay minh họa.

## Rule: Mỗi bài Facebook PHẢI có ảnh đi kèm

Khi tạo Facebook post, LUÔN tạo ảnh minh họa đi kèm. Bài viết Facebook không có ảnh sẽ bị giảm reach đáng kể. Skill này nên được gọi tự động sau khi tạo xong nội dung bài viết Facebook.

## Workflow

**QUAN TRỌNG:** Luôn tuân theo `references/workflow.md` khi skill được kích hoạt.

## Input

Nội dung bài viết Facebook (tiếng Việt) hoặc chủ đề + key points.

## Design System (Bắt buộc cho MỌI dạng ảnh)

### Palette

| Element | Value | Mô tả |
|---------|-------|--------|
| Background | `#F5F0E8` | Cream/off-white, paper texture nhẹ |
| Text | `#1A1A1A` | Near-black, dễ đọc |
| Highlight | `#FFE066` | Yellow marker highlight effect |
| Underline | `#C0392B` | Red double underline cho key phrase |
| Accent (optional) | `#6B9E7A` | Sage green cho icon/border infographic |
| Footer text | `#666666` | Gray nhạt cho chữ ký |

### Typography

- **Font**: Clean sans-serif (Montserrat, Inter, hoặc tương đương)
- **Title**: Bold, 28-36px equivalent, UPPERCASE nếu là infographic
- **Body**: Regular/Medium, 20-24px equivalent
- **Emphasis**: Bold cho từ quan trọng
- **Footer**: Small subtle text, centered, `@tranvanhoang.com` (IMPORTANT: do NOT include pixel sizes like "16px" or "18px" in the prompt — AI models render the literal text into the image)

### Visual Emphasis (2 kỹ thuật chính)

1. **Yellow Highlight Marker** — Dùng cho tiêu đề, từ tích cực, keyword chính. Hiệu ứng như bút highlight tay.
2. **Red Double Underline** — Dùng cho takeaway cuối, từ cảnh báo, kết luận quan trọng. Gạch chân đỏ đôi.

### Layout Rules

- Aspect ratio: **1:1** (1080x1080 hoặc 2K equivalent)
- Padding: 80-100px mỗi bên
- Footer: `@tranvanhoang.com` centered, cách bottom 60px
- Spacing giữa các dòng: 1.6-1.8 line-height
- NO photos, NO complex illustrations — chỉ text + simple icons nếu cần

---

## 6 Dạng Ảnh

### 1. Progressive / Escalation (Leo thang)

**Khi nào dùng:** Bài viết có chuỗi câu giảm dần/tăng dần scope, Q&A pattern, hoặc "không X thì Y".

**Cấu trúc:**
```
[Title — yellow highlight]
  • Bullet 1
  • Bullet 2
  • Bullet 3

Câu hỏi 1?
Đáp 1.

Câu hỏi 2?
Đáp 2.

...

[Kết luận — bold + red double underline]

@tranvanhoang.com
```

**Prompt mẫu:**
```
A clean typographic image on cream paper texture background (#F5F0E8).

Title at top: "[TIÊU ĐỀ]" in bold black sans-serif font with yellow highlight marker effect behind the text.

Below the title, a bullet list:
• [Item 1]
• [Item 2]
• [Item 3]

Then a series of question-answer pairs in decreasing scope:
"[Câu hỏi 1]?"
"[Đáp 1]."

"[Câu hỏi 2]?"
"[Đáp 2]."

"[Câu hỏi 3]?"
"[Đáp 3]."

At the bottom, a closing statement: "[KẾT LUẬN]" in bold with red double underline on the key phrase "[KEYWORD]".

Footer centered at bottom: "@tranvanhoang.com" in small gray text.

Style: Minimal, professional, knowledge-sharing aesthetic. Clean sans-serif typography. NO photos, NO illustrations, ONLY text. Paper texture background. Square format 1:1.
NEVER add watermarks. NEVER add random decorative elements.
```

---

### 2. Contrast Pairs (Đối lập)

**Khi nào dùng:** Bài viết có cặp đối lập "X nhưng không Y", "Nên X, đừng Y", hai mặt của vấn đề.

**Cấu trúc:**
```
[Từ tích cực — yellow highlight], nhưng không [từ cảnh báo — red underline].
[Từ tích cực — yellow highlight], nhưng không [từ cảnh báo — red underline].
...

@tranvanhoang.com
```

**Prompt mẫu:**
```
A clean typographic image on cream paper texture background (#F5F0E8).

Centered vertically, a series of [N] parallel sentences, each on its own line with generous spacing between lines:

"[Từ 1a]" (with yellow highlight marker effect), nhưng không "[từ 1b]" (bold with red double underline).
"[Từ 2a]" (with yellow highlight marker effect), nhưng không "[từ 2b]" (bold with red double underline).
"[Từ 3a]" (with yellow highlight marker effect), nhưng không "[từ 3b]" (bold with red double underline).
"[Từ 4a]" (with yellow highlight marker effect), nhưng không "[từ 4b]" (bold with red double underline).
"[Từ 5a]" (with yellow highlight marker effect), nhưng không "[từ 5b]" (bold with red double underline).
"[Từ 6a]" (with yellow highlight marker effect), nhưng không "[từ 6b]" (bold with red double underline).

Font: Bold sans-serif, 24-28px equivalent. Each line centered horizontally.

Footer centered at bottom: "@tranvanhoang.com" in small gray text.

Style: Minimal, elegant, knowledge-sharing aesthetic. Clean typography on paper texture. NO photos, NO illustrations, ONLY text. Square format 1:1.
NEVER add watermarks. NEVER add random decorative elements.
```

---

### 3. Multi-column Infographic (Bảng thông tin)

**Khi nào dùng:** Bài viết có 2-3 nhóm thông tin, tips theo category, phân loại rõ ràng.

**Cấu trúc:**
```
[TIÊU ĐỀ LỚN — bold uppercase]
[Phụ đề]

| Cột 1 Header    | Cột 2 Header    | Cột 3 Header    |
| icon + item 1   | icon + item 1   | Card box 1      |
| icon + item 2   | icon + item 2   | Card box 2      |
| icon + item 3   | icon + item 3   |                  |
| icon + item 4   | icon + item 4   |                  |

@tranvanhoang.com
```

**Prompt mẫu:**
```
A clean infographic image on cream/off-white background (#F5F0E8).

Large bold title at top: "[TIÊU ĐỀ]" in uppercase black sans-serif.
Subtitle below: "[Phụ đề]" in lighter weight.

Layout: 3 equal columns separated by thin lines.

Column 1 — "[Header 1]" in bold uppercase sage green (#6B9E7A):
- Brain icon + "[Item 1]" in bold uppercase
- Clock icon + "[Item 2]" in bold uppercase
- Smiley icon + "[Item 3]" in bold uppercase
- Moon icon + "[Item 4]" in bold uppercase
- Running icon + "[Item 5]" in bold uppercase

Column 2 — "[Header 2]" in bold uppercase sage green:
- Green checkmark + "[Item 1]" in bold uppercase
- Green checkmark + "[Item 2]" in bold uppercase
- Green checkmark + "[Item 3]" in bold uppercase
- Green checkmark + "[Item 4]" in bold uppercase

Column 3 — "[Header 3]" in bold uppercase sage green:
- Rounded rectangle card with sage green border containing icon + "[Item 1]" text
- Rounded rectangle card with sage green border containing icon + "[Item 2]" text

Icons: Simple line-art style, sage green color (#6B9E7A). Minimal, consistent stroke weight.

Footer centered at bottom: "@tranvanhoang.com" in small gray text.

Style: Clean, professional infographic. Sage green accent color. Simple icons. NO photos. Square format 1:1.
NEVER add watermarks. NEVER add random decorative elements beyond the described icons.
```

---

### 4. Numbered List (Danh sách đánh số)

**Khi nào dùng:** Bài viết liệt kê tips, bước làm, sai lầm, lý do — có số thứ tự rõ.

**Cấu trúc:**
```
[Title — yellow highlight]

1. [Item 1]
2. [Item 2]
3. [Item 3]
...

[Kết luận — bold + red underline]

@tranvanhoang.com
```

**Prompt mẫu:**
```
A clean typographic image on cream paper texture background (#F5F0E8).

Title at top: "[TIÊU ĐỀ]" in bold black sans-serif with yellow highlight marker effect.

Below, a numbered list with generous spacing:
1. "[Item 1]" — bold number, regular text
2. "[Item 2]"
3. "[Item 3]"
4. "[Item 4]"
5. "[Item 5]"

Each number is bold and slightly larger. Text is clean sans-serif.

Optional closing line at bottom: "[KẾT LUẬN]" in bold, key phrase has red double underline.

Footer centered at bottom: "@tranvanhoang.com" in small gray text.

Style: Minimal, professional knowledge-sharing. Paper texture background. NO photos, NO illustrations. Square format 1:1.
NEVER add watermarks. NEVER add random decorative elements.
```

---

### 5. Quote / Statement (Câu nói / Nhận định)

**Khi nào dùng:** Bài viết có 1 câu nói mạnh, insight đơn lẻ, mindset shift, hoặc trích dẫn.

**Cấu trúc:**
```
"[Câu nói chính — large bold text]"

[Giải thích ngắn — smaller text, optional]

@tranvanhoang.com
```

**Prompt mẫu:**
```
A clean typographic image on cream paper texture background (#F5F0E8).

Centered both vertically and horizontally, a powerful statement in large bold black sans-serif:
"[CÂU NÓI CHÍNH]"

Key word "[KEYWORD]" has yellow highlight marker effect. The concluding word "[KEYWORD 2]" has red double underline.

Optionally, a smaller explanatory line below in regular weight gray text:
"[Giải thích ngắn]"

Footer centered at bottom: "@tranvanhoang.com" in small gray text.

Style: Minimal, impactful. Large typography dominates the frame. Lots of white space. Paper texture background. NO photos, NO illustrations. Square format 1:1.
NEVER add watermarks. NEVER add random decorative elements.
```

---

### 6. Before/After (Trước & Sau)

**Khi nào dùng:** Bài viết so sánh trước/sau khi áp dụng, cũ vs mới, sai vs đúng.

**Cấu trúc:**
```
[TIÊU ĐỀ]

❌ Trước / Sai:          ✅ Sau / Đúng:
- Item 1                  - Item 1
- Item 2                  - Item 2
- Item 3                  - Item 3

@tranvanhoang.com
```

**Prompt mẫu:**
```
A clean typographic comparison image on cream paper texture background (#F5F0E8).

Title at top center: "[TIÊU ĐỀ]" in bold black sans-serif with yellow highlight.

Split into two columns:

LEFT column with red accent header "❌ [LABEL TRÁI]":
- "[Item 1]" with strikethrough or dimmed text
- "[Item 2]"
- "[Item 3]"

RIGHT column with green accent header "✅ [LABEL PHẢI]":
- "[Item 1]" in bold confident text
- "[Item 2]"
- "[Item 3]"

A thin vertical divider line between columns. Left side slightly muted/gray tone, right side clearer/bolder.

Footer centered at bottom: "@tranvanhoang.com" in small gray text.

Style: Clean comparison layout. Minimal design. Paper texture. NO photos. Square format 1:1.
NEVER add watermarks. NEVER add random decorative elements.
```

---

## Auto-Classification

Khi nhận bài viết, phân loại tự động theo bảng sau:

| Dấu hiệu trong bài | Dạng ảnh |
|---------------------|----------|
| Chuỗi câu hỏi-đáp giảm dần, "không X thì Y" | **Progressive** |
| Cặp đối lập "X nhưng không Y", "nên X đừng Y" | **Contrast Pairs** |
| 2-3 nhóm category rõ ràng, phân loại tips | **Multi-column Infographic** |
| Liệt kê 3-10 items có số thứ tự | **Numbered List** |
| 1 câu nói mạnh, insight, quote, mindset | **Quote / Statement** |
| So sánh trước/sau, sai/đúng, cũ/mới | **Before/After** |

## Process

1. **Phân tích nội dung** — Đọc bài viết, xác định chủ đề + thông điệp chính
2. **Auto-classify** — Dùng bảng trên để chọn dạng ảnh phù hợp nhất
3. **Extract content** — Rút trích text chính xác cho từng element (title, items, conclusion...)
4. **Build prompt** — Dùng prompt mẫu tương ứng, điền nội dung Vietnamese chính xác
5. **Xác nhận** — Trình bày phân tích + prompt, hỏi user confirm
6. **Generate** — Tạo ảnh

## Generate

```bash
cd .claude/skills/image-post-creator && python3 scripts/generate.py "<prompt>" -o ./generated-$(date +%Y%m%d-%H%M%S).png -ar 1:1 --size 2K -v
```

### Options

| Flag | Description |
|------|-------------|
| `-o, --output` | Output path (required) |
| `-ar, --aspect-ratio` | Default: 1:1 (square cho Facebook) |
| `--size` | 1K, 2K, 4K (default: 2K) |
| `-v, --verbose` | Show details |
| `--dry-run` | Show prompt without generating |

## Confirm Step

Trước khi generate, trình bày:

1. **Dạng ảnh**: [tên dạng]
2. **Content extracted**: Các text element sẽ xuất hiện trên ảnh
3. **Prompt**: Full prompt

```json
{"questions": [
  {"question": "Bạn muốn tạo ảnh với prompt này?", "header": "Xác nhận", "multiSelect": false, "options": [
    {"label": "Tạo luôn (Recommended)", "description": "Tạo ảnh với prompt trên"},
    {"label": "Sửa prompt", "description": "Chỉnh sửa prompt trước khi tạo"},
    {"label": "Đổi dạng ảnh", "description": "Chọn dạng thể hiện khác"},
    {"label": "Chỉ lấy prompt", "description": "Copy prompt, không tạo ảnh"}
  ]}
]}
```

## Output

```
✅ Ảnh đã tạo: [path]
   Dạng: [Progressive/Contrast Pairs/Multi-column/Numbered List/Quote/Before-After]
   Aspect: 1:1
   Footer: @tranvanhoang.com

Prompt đã dùng:
[full prompt]
```

## Error Handling

| Lỗi | Xử lý |
|------|--------|
| API key missing | Hướng dẫn set GEMINI_API_KEY |
| Text render sai tiếng Việt | Retry với instruction "Vietnamese diacritics MUST be accurate" |
| Không xác định được dạng ảnh | Hỏi user chọn từ 6 dạng |
| Nội dung quá dài cho 1 ảnh | Đề xuất tách thành 2 ảnh carousel |

## References

| Topic | File |
|-------|------|
| **Main Workflow** | `references/workflow.md` |
| Nano Banana Guide | `references/nano-banana.md` |
| Image Prompting | `references/image-prompting.md` |
