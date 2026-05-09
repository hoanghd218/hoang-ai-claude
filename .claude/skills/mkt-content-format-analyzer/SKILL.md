---
name: mkt-content-format-analyzer
description: Analyze transcripts or content to classify them into the 4A content framework (Actionable, Analytical, Aspirational, Anthropological). Use when analyzing YouTube transcripts, blog posts, social media content, or any text to determine its content format and approach. Input is transcript text; output is the primary 4A category and specific content format classification.
---

# Content Format Analyzer

Phân tích transcript/content và đưa ra đánh giá chi tiết theo **4A Framework** + **220 Proven Viral Formats**.

## References

- [4A Framework](references/4a_framework.md) - Framework phân loại nội dung theo 4 nhóm
- [220 Viral Formats](references/220_viral_formats.md) - Bộ sưu tập 220 định dạng video đã chứng minh viral

---

## Output Format

```
📊 4A FRAMEWORK: [ACTIONABLE/ANALYTICAL/ASPIRATIONAL/ANTHROPOLOGICAL]
[Mô tả ngắn 1-2 dòng về nội dung - phân tích chi tiết về chủ đề chính]

� VIRAL FORMAT PHÙ HỢP:
• #[ID] [Tên format] - [Mô tả ngắn áp dụng cho content]
• #[ID] [Tên format] - [Mô tả ngắn áp dụng cho content]
• #[ID] [Tên format] - [Mô tả ngắn áp dụng cho content]
• #[ID] [Tên format] - [Mô tả ngắn áp dụng cho content]

🪝 GỢI Ý HOOK:
• "[Hook suggestion 1]"
• "[Hook suggestion 2]"
• "[Hook suggestion 3]"
```

---

## Quick Reference

| 4A Category | Câu hỏi nhận diện |
|-------------|-------------------|
| **Actionable** | Giúp người xem LÀM gì đó? |
| **Analytical** | Giúp người xem HIỂU sâu hơn? |
| **Aspirational** | Khơi gợi CẢM XÚC mạnh? |
| **Anthropological** | Đưa ra GÓC NHÌN độc đáo? |

→ Chi tiết: [4a_framework.md](references/4a_framework.md) | [220_viral_formats.md](references/220_viral_formats.md)

---

## Example Output

**Input**: Transcript video so sánh bê tông tươi vs bê tông đổ tay

```
📊 4A FRAMEWORK: ANALYTICAL
So sánh ưu nhược điểm bê tông tươi vs bê tông đổ tay - phân tích chi tiết về thời gian, chất lượng, điều kiện thi công.

🎯 VIRAL FORMAT PHÙ HỢP:
• #24 Side-by-Side Comparison - So sánh 2 loại bê tông
• #94 Deep Dive Explainer - Phân tích ưu nhược điểm
• #62 Myth-Busting - Loại nào tốt hơn?
• #47 Pro Tips - Tùy điều kiện chọn loại phù hợp

🪝 GỢI Ý HOOK:
• "Bê tông tươi hay đổ tay - chọn loại nào?"
• "Ưu nhược điểm bê tông tươi vs đổ tay"
• "Loại bê tông nào tốt hơn khi xây nhà?"
```
