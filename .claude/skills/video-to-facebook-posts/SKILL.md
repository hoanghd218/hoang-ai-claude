---
name: video-to-facebook-posts
description: Analyze knowledge-sharing video transcripts and generate up to 3 Facebook posts. Auto-detects content type (knowledge listing vs comparative analysis) and produces actionable posts or comparison posts following Hoang's brand voice. Input is video title + transcript. Output is analysis + Facebook posts in Vietnamese.
---

# Video to Facebook Posts

Phân tích transcript video chia sẻ kiến thức, tự động nhận diện loại nội dung, và tạo tối đa 3 bài viết Facebook theo brand voice của Hoàng.

## Brand Voice Reference

- [BRANDVOICE.MD](../../../MY RESOURCES/BRANDVOICE.MD) - DNA Brand Voice Hoàng

**Quy tắc bắt buộc khi viết:**
- Xưng hô: "Hoàng" / "mình", gọi người đọc: "bạn", "các bạn"
- Giọng: Conversational expert, 7/10 energy - tự tin, sắc bén, truyền cảm hứng hành động
- Nhịp điệu: Phối hợp câu ngắn, trung bình, dài - không đều đều
- Power words giữ tiếng Anh: System, Automation, AI, Framework, Workflow, Template, Scale
- Luôn có số liệu cụ thể, case study thực tế
- Kết thúc bằng CTA rõ ràng

## Workflow

### Phase 1: Thu thập thông tin

Khi user gọi skill, cần 2 input bắt buộc:

1. **Tiêu đề video** - Tên video gốc
2. **Transcript** - Nội dung transcript đầy đủ

Nếu thiếu, hỏi user trước khi tiếp tục.

### Phase 2: Phân tích nội dung

Đọc toàn bộ transcript và phân tích theo [Analysis Framework](references/analysis_framework.md):

**Bước 1 - Nhận diện loại nội dung:**

| Loại | Dấu hiệu nhận biết | Ví dụ |
|------|---------------------|-------|
| **Liệt kê kiến thức** | Liệt kê tips, steps, tools, features, hướng dẫn từng bước | "5 cách dùng AI", "Hướng dẫn setup Claude Code" |
| **Phân tích so sánh** | So sánh A vs B, ưu nhược điểm, phân tích sâu, đánh giá | "Agent Teams vs Sub Agents", "ChatGPT vs Claude" |
| **Hybrid** | Vừa liệt kê vừa so sánh - khi có cả 2 yếu tố rõ ràng | "3 loại agent trong Claude Code - khác nhau thế nào?" |

**Bước 2 - Trích xuất key insights:**
- Các điểm chính (main points) từ transcript
- Số liệu, data, case study cụ thể
- Quotes hay, câu nói đáng nhớ
- Pain points & solutions được đề cập
- Kết luận / recommendation của video

**Bước 3 - Xác định góc viết Facebook:**
- Mỗi bài viết phải có **góc nhìn (lens) riêng biệt** - không lặp lại cùng một góc
- Tối đa 3 bài, mỗi bài khai thác một khía cạnh khác nhau của video

### Phase 3: Tạo bài viết Facebook

Dựa trên kết quả phân tích, tạo **tối đa 3 bài viết** theo [Post Templates](references/post_templates.md).

**Quy tắc chọn format:**

| Loại nội dung | Format bài viết phù hợp |
|---------------|------------------------|
| Liệt kê kiến thức | Actionable Post, Listicle Post |
| Phân tích so sánh | Comparison Post, Deep-dive Post |
| Hybrid | Mix - 1 Comparison + 1-2 Actionable |

**Quy tắc viết bắt buộc:**
1. Hook 2 dòng đầu phải gây tò mò / shock - quyết định người đọc có đọc tiếp không
2. Không mở đầu kiểu "Hôm nay mình chia sẻ..." - đi thẳng vào vấn đề
3. **KHÔNG dùng emoji, icon, ký tự đặc biệt** trong bài viết (không dùng ✅, ❌, 🔴, 🟡, 🟢, 🔵, →, •, 1️⃣, ═, hay bất kỳ ký tự Unicode đặc biệt nào). Chỉ dùng text thuần, dấu gạch ngang (-), dấu chấm, dấu phẩy, dấu hai chấm
4. Có line breaks rõ ràng - dễ đọc trên mobile
5. Kết thúc bằng CTA + Last Dab (câu chốt hạ đáng nhớ)
6. Mỗi bài 300-600 từ - đủ sâu nhưng không quá dài cho Facebook

## Output Format

```
═══════════════════════════════════════
📊 PHÂN TÍCH TRANSCRIPT
═══════════════════════════════════════

🎬 Video: [Tiêu đề video]
📌 Loại nội dung: [Liệt kê kiến thức / Phân tích so sánh / Hybrid]

🔑 Key Insights:
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]
...

📊 Số liệu nổi bật: [Nếu có]
💡 Góc nhìn độc đáo: [Lens riêng của video]

═══════════════════════════════════════
✍️ BÀI VIẾT #1: [Tên bài / Góc khai thác]
Format: [Actionable / Comparison / Listicle / Deep-dive]
═══════════════════════════════════════

[Nội dung bài viết Facebook đầy đủ - copy-paste ready]

---

═══════════════════════════════════════
✍️ BÀI VIẾT #2: [Tên bài / Góc khai thác]
Format: [Actionable / Comparison / Listicle / Deep-dive]
═══════════════════════════════════════

[Nội dung bài viết Facebook đầy đủ - copy-paste ready]

---

═══════════════════════════════════════
✍️ BÀI VIẾT #3: [Tên bài / Góc khai thác]
Format: [Actionable / Comparison / Listicle / Deep-dive]
═══════════════════════════════════════

[Nội dung bài viết Facebook đầy đủ - copy-paste ready]
```

## Mandatory Rules

### Phân tích
- Đọc TOÀN BỘ transcript - không bỏ sót
- Trích xuất insight chính xác từ nội dung - không bịa
- Phân loại đúng loại nội dung dựa trên dấu hiệu cụ thể

### Viết bài
- **PHẢI** đọc và áp dụng brand voice từ BRANDVOICE.MD
- Mỗi bài có góc nhìn khác nhau - không lặp lại
- Hook phải tạo được "gap" hoặc "shock" trong 2 dòng đầu
- Cấu trúc The Dance: Bối cảnh → Nhưng (xung đột) → Vì vậy (giải pháp)
- Luôn có con số cụ thể nếu transcript cung cấp
- Viết tiếng Việt tự nhiên, conversational - không máy móc
- CTA phù hợp ngữ cảnh (mềm/trung bình/mạnh)

### Output
- Bài viết phải copy-paste ready - không cần chỉnh sửa thêm
- Lưu output vào `workspace/content/facebook/` nếu user yêu cầu save
- Tên file: `[slug-tiêu-đề]-facebook-posts.md`

## Example

**Input:**
- Tiêu đề: "Claude Code Agent Teams - Hướng dẫn setup và sử dụng"
- Transcript: [nội dung video hướng dẫn về 3 chế độ trong Claude Code: default, sub agents, agent teams]

**Phân tích:**
- Loại: Hybrid (vừa liệt kê 3 modes, vừa so sánh ưu nhược điểm)
- Key insights: default = 1 context, sub agents = parallel nhưng không giao tiếp, agent teams = parallel + giao tiếp

**Output 3 bài:**
1. **Comparison Post**: "Default vs Sub Agents vs Agent Teams - chọn cái nào?"
2. **Actionable Post**: "Cách setup Agent Teams trong 5 phút"
3. **Deep-dive Post**: "Tại sao Agent Teams thay đổi cách code của mình"
