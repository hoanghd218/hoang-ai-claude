---
name: mkt-linkedin-post-creator
description: Create LinkedIn posts in ENGLISH optimized for global professional audience. Auto-detect content type, choose best format (Insight, Case Study, Contrarian, Carousel Text). Output in English with Hoàng's brand voice adapted for LinkedIn. USE WHEN user says 'tạo post linkedin', 'viết linkedin', 'linkedin post', 'bài linkedin', 'viết cho linkedin', 'post cho linkedin'.
---

# LinkedIn Post Creator

Create posts for LinkedIn in **ENGLISH** — optimized for global professional audience. Professional tone with credential signals, position Hoàng as AI consultant/builder.

## Content Language Rule

**LinkedIn content MUST be written in English.** Only Facebook and YouTube use Vietnamese. LinkedIn, X.com, and Instagram all use English for global reach.

## Brand Voice Reference

- [BRANDVOICE.MD](../../../MY RESOURCES/BRANDVOICE.MD) - DNA Brand Voice Hoàng (adapt to English)

**Brand voice adapted for LinkedIn (English):**
- Voice: "I" / "Hoang" — first person, professional
- Address readers: "you"
- Tone: Professional expert — conversational but with depth and credentials
- Energy: 6.5/10 — confident, thoughtful, less hype than Facebook
- Credential signals: "After 2 years implementing AI for businesses...", "From consulting 50+ SMEs..."
- Power words: System, Automation, AI, Framework, Workflow, ROI, Strategy, Implementation, Enterprise, Scale
- Always include data and real case studies
- NO emoji in body text

## Platform Rules — LinkedIn

| Rule | Detail |
|------|--------|
| Optimal length | 1300-2000 ký tự (LinkedIn sweet spot Vietnamese) |
| First 2 lines | PHẢI hook — đây là phần hiển thị trước "see more" |
| Hashtags | 3-5 hashtags, cuối bài sau 1 line break |
| Formatting | Line breaks rõ ràng, bullet points dạng text thuần (dùng - hoặc số) |
| Tone | Professional-conversational, credential-heavy, industry framing |
| CTA style | Soft — "Follow để xem thêm", "Bạn nghĩ sao?", "Comment chia sẻ" |
| Image/Doc | Suggest kèm image hoặc PDF carousel nếu phù hợp |

## Workflow

### Phase 1: Thu thập thông tin

Khi user gọi skill, cần ít nhất 1 input:

1. **Transcript** — Nội dung transcript video
2. **Topic + Insight** — Chủ đề + insight cụ thể
3. **Bài viết Facebook** — Adapt từ bài FB sang LinkedIn format
4. **Case study / số liệu** — Kết quả dự án, data thực tế

Nếu thiếu, hỏi user trước khi tiếp tục.

### Phase 2: Phân tích & chọn format

Đọc input và phân tích:

**Bước 1 — Nhận diện loại nội dung phù hợp LinkedIn:**

| Loại | Dấu hiệu | Best Format |
|------|-----------|-------------|
| Industry insight, trend | Data, research, prediction | Insight Post |
| Kết quả dự án, implementation | Số liệu before/after, steps | Case Study Post |
| Counter-intuitive, opinion | Quan điểm mạnh, phản bác | Contrarian Take |
| Multi-point, educational | Nhiều tips/lessons, list format | Carousel Text Post |

**Bước 2 — Trích xuất key points:**
- Professional angle (góc nhìn industry/business)
- Credential context (kinh nghiệm, data, authority)
- Actionable insight (bài học áp dụng được)
- Discussion trigger (câu hỏi mở cho engagement)

**Bước 3 — Chọn format:**
Tạo 1-2 posts, mỗi post một format khác nhau.

### Phase 3: Tạo content

Dựa trên phân tích, tạo content theo [Post Templates](references/post-templates.md) và [Tone Guide](references/tone-guide.md).

**Quy tắc viết bắt buộc:**
1. 2 dòng đầu PHẢI hook — hiển thị trước "see more", quyết định CTR
2. Credential signal trong 3 dòng đầu — tại sao người đọc nên tin bạn
3. KHÔNG dùng emoji, icon, ký tự đặc biệt
4. Line breaks rõ ràng — dễ scan trên mobile
5. Hashtags cuối bài, 3-5 tags, sau 1 line break trống
6. 1300-2000 ký tự — đủ sâu cho LinkedIn audience
7. CTA mềm — LinkedIn không phải nơi hard sell

## Output Format

```
═══════════════════════════════════════
PHAN TICH INPUT
═══════════════════════════════════════

Source: [Tiêu đề / chủ đề]
Loại nội dung: [Insight / Case Study / Contrarian / Educational]
Format chọn: [Post type]
Professional angle: [Góc nhìn industry]

═══════════════════════════════════════
LINKEDIN POST #1: [Tiêu đề / Góc khai thác]
Format: [Insight / Case Study / Contrarian / Carousel Text]
Chars: [Số ký tự]
═══════════════════════════════════════

[Nội dung LinkedIn post — copy-paste ready]

[hashtags]

═══════════════════════════════════════
LINKEDIN POST #2 (nếu có): [Tiêu đề / Góc khai thác]
═══════════════════════════════════════

[Nội dung]
```

## Mandatory Rules

### Phân tích
- Đọc TOÀN BỘ input — không bỏ sót
- Trích xuất insight chính xác — không bịa
- Tìm professional/business angle cho mọi topic

### Viết
- **PHẢI** đọc và áp dụng brand voice từ BRANDVOICE.MD (với điều chỉnh LinkedIn)
- **PHẢI** đọc tone guide tại references/tone-guide.md
- 2 dòng đầu = hook, phải work khi bị cắt bởi "see more"
- Credential signal sớm trong bài
- Tone professional — không casual quá nhưng không corporate boring
- Vietnamese có dấu đầy đủ, giữ English tech terms
- Kết thúc bằng câu hỏi mở hoặc soft CTA — không hard sell

### Output
- Content phải copy-paste ready
- Lưu output vào `workspace/content/linkedin/` nếu user yêu cầu save
- Tên file: `[slug]-linkedin-posts.md`

## Example

**Input:**
- Topic: AI Agent automation cho doanh nghiệp nhỏ
- Insight: 1 người + AI agents = output cả team, tiết kiệm 70% chi phí nhân sự

**Output:**

LinkedIn Post — Case Study format:

```
Tôi vừa giúp một doanh nghiệp 5 người cắt giảm 70% chi phí vận hành.
Không phải sa thải — mà là automation.

Sau 2 năm triển khai AI systems cho SMEs, pattern lặp đi lặp lại:

Doanh nghiệp nhỏ không thiếu người.
Họ thiếu hệ thống.

Case cụ thể:
- Trước: 3 nhân viên xử lý email, báo giá, chăm sóc khách hàng — 8h/ngày
- Sau: 1 AI Agent workflow xử lý 80% tự động — 3 người đó focus vào việc tạo ra revenue

Kết quả sau 3 tháng:
- Thời gian response khách hàng: từ 2 giờ xuống 5 phút
- Chi phí vận hành giảm 70%
- Revenue tăng 40% vì team focus đúng việc

Bài học lớn nhất: AI không thay thế con người. AI giải phóng con người khỏi những việc không ai muốn làm.

Doanh nghiệp bạn đang tốn bao nhiêu giờ/tuần cho việc lặp lại?

#AI #Automation #SME #DigitalTransformation #AIVietnam
```
