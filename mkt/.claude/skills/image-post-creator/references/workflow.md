# Image Post Creator Workflow

Agent instructions for creating knowledge-sharing images for Facebook posts.

## Step 1: Nhận nội dung

Yêu cầu user cung cấp nội dung bài viết Facebook (copy-paste toàn bộ bài viết hoặc key points).

Nếu user đã cung cấp → chuyển sang Step 2.

## Step 2: Phân tích & Auto-classify

Đọc kỹ bài viết và xác định:

1. **Chủ đề chính** — Bài viết nói về cái gì?
2. **Thông điệp cốt lõi** — Điều quan trọng nhất muốn truyền tải?
3. **Dạng ảnh** — Tự động phân loại theo bảng:

| Dấu hiệu | Dạng ảnh |
|-----------|----------|
| Chuỗi câu hỏi-đáp giảm dần, "không X thì Y" | **Progressive** |
| Cặp đối lập "X nhưng không Y", "nên X đừng Y" | **Contrast Pairs** |
| 2-3 nhóm category rõ ràng, phân loại tips | **Multi-column Infographic** |
| Liệt kê 3-10 items có số thứ tự | **Numbered List** |
| 1 câu nói mạnh, insight, quote, mindset | **Quote / Statement** |
| So sánh trước/sau, sai/đúng, cũ/mới | **Before/After** |

## Step 3: Extract content

Rút trích text chính xác từ bài viết cho từng element:

- **Title**: Tiêu đề / câu chính
- **Items**: Danh sách các điểm
- **Conclusion**: Kết luận / takeaway
- **Keywords to highlight**: Từ nào cần yellow highlight, từ nào cần red underline

**Quy tắc highlight:**
- Yellow highlight → tiêu đề, từ tích cực, keyword chính
- Red double underline → takeaway cuối cùng, từ cảnh báo, kết luận quan trọng

## Step 4: Build prompt

Dùng prompt mẫu từ SKILL.md tương ứng với dạng ảnh đã chọn.

### Design System (BẮT BUỘC trong mọi prompt):

```
Background: cream paper texture (#F5F0E8)
Font: clean sans-serif (Montserrat/Inter style)
Yellow highlight marker effect on: [specified words]
Red double underline on: [specified words]
Footer: "@tranvanhoang.com" centered at bottom in small gray text
Aspect: 1:1 square
Style: Minimal, professional, knowledge-sharing
NO photos, NO illustrations (unless infographic icons)
NEVER add watermarks. NEVER add random decorative elements.
```

### Vietnamese text accuracy

Luôn thêm vào prompt:
```
ALL Vietnamese text MUST have accurate diacritics. Double-check: ă, â, ơ, ư, ê, ô, đ and all tone marks (sắc, huyền, hỏi, ngã, nặng).
```

## Step 5: Xác nhận với user

Trình bày:

1. **Dạng ảnh**: [tên dạng] + lý do chọn
2. **Text elements**: Liệt kê chính xác text sẽ xuất hiện trên ảnh
3. **Highlight plan**: Từ nào yellow, từ nào red underline
4. **Full prompt**: Prompt đầy đủ

Dùng `AskUserQuestion` để confirm.

## Step 6: Generate

```bash
cd .claude/skills/image-post-creator && python3 scripts/generate.py "<prompt>" \
  -o ./generated-$(date +%Y%m%d-%H%M%S).png \
  -ar 1:1 \
  --size 2K \
  -v
```

**Model**: Nano Banana Pro (`gemini-3.1-flash-image-preview` hoặc `gemini-3-pro-image-preview`).

## Step 7: Review & Iterate

Sau khi generate, hiển thị ảnh cho user review.

Nếu text render sai tiếng Việt → retry với thêm emphasis:
```
CRITICAL: Vietnamese diacritics MUST be pixel-perfect accurate. The word "[sai]" must be spelled exactly as "[đúng]".
```

Nếu layout không đúng → adjust prompt và retry.

## Step 8: Output

```
✅ Ảnh đã tạo: [path]
   Dạng: [tên dạng]
   Aspect: 1:1
   Footer: @tranvanhoang.com

Prompt đã dùng:
[full prompt]
```
