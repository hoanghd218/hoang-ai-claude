---
name: mkt-video-to-content-idea
description: Analyze video content and generate Facebook content ideas (step-by-step posts, actionable posts, tech news posts). Input is video name + transcript + insight. Output is structured analysis with content drafts in Vietnamese. USE WHEN user says 'phân tích video làm content', 'video to content idea', 'gợi ý content từ video', 'chuyển video thành bài facebook', 'content idea từ transcript', 'video nào làm content được', 'đánh giá video làm content'.
---

# Video to Content Idea

Phân tích video dựa trên thông tin được cung cấp (tiêu đề, transcript, insight), đánh giá tiềm năng và gợi ý cách chuyển thành nội dung Facebook phù hợp cho audience AI/Tech/Automation.

## Brand Voice Reference

- [BRANDVOICE.MD](../../../MY RESOURCES/BRANDVOICE.MD) - DNA Brand Voice Hoàng

**Quy tắc bắt buộc khi viết:**
- Xưng hô: "Hoàng" / "mình", gọi người đọc: "bạn", "các bạn"
- Giọng: Conversational expert, 7/10 energy - tự tin, sắc bén, truyền cảm hứng hành động
- Nhịp điệu: Phối hợp câu ngắn, trung bình, dài - không đều đều
- Power words giữ tiếng Anh: System, Automation, AI, Framework, Workflow, Template, Scale
- Luôn có số liệu cụ thể, case study thực tế
- Kết thúc bằng CTA rõ ràng
- KHÔNG dùng emoji, icon, ký tự đặc biệt trong bài viết

---

## Ngôn ngữ output

**BẮT BUỘC: Toàn bộ output tiếng Việt phải CÓ DẤU đầy đủ.**

Ví dụ đúng: "Bạn đang dùng AI như một chatbot. Nhưng những người hiểu chuyện đang đối xử với nó như một nhân viên mới."

**BẮT BUỘC: Viết đơn giản, dễ hiểu -- học sinh lớp 5 cũng hiểu được.**

Quy tắc viết đơn giản:
- Dùng từ ngắn, phổ thông. Tránh từ hàn lâm, chuyên ngành trừ khi cần thiết.
- Mỗi câu tối đa 15-20 từ. Câu dài phải tách ra.
- Giải thích thuật ngữ tiếng Anh ngay khi dùng lần đầu. Ví dụ: "MCP (cầu nối giúp AI nói chuyện với các app khác)"
- Dùng ví dụ đời thường, so sánh gần gũi. Ví dụ: "Giống như bạn thuê một nhân viên mới -- bạn phải cho họ đọc sổ tay công ty trước khi làm việc."
- Tránh câu bị động, câu phủ định kép.
- Viết như đang nói chuyện với bạn bè, không phải viết luận văn.

---

## Input

Khi user gọi skill, cần 3 input:

1. **Tiêu đề video** (bắt buộc) - Tên video gốc
2. **Transcript** (bắt buộc) - Nội dung transcript đầy đủ
3. **Insight đã trích xuất** (tuỳ chọn) - Danh sách insight nếu có
4. **Số lượt xem** (tuỳ chọn) - Số view nếu có

Nếu thiếu tiêu đề hoặc transcript, hỏi user trước khi tiếp tục.

---

## Process

### Bước 1: Tóm tắt nội dung chính

Tóm tắt video trong 3-5 câu. Nêu rõ:
- Chủ đề chính
- Đối tượng mục tiêu
- Giá trị cốt lõi mà video mang lại

### Bước 2: Trích xuất "Knowledge Nuggets"

Liệt kê tất cả các đơn vị kiến thức có thể tách ra làm content độc lập:

| Loại | Dấu hiệu |
|------|----------|
| Framework / Mô hình | Có cấu trúc, quy trình, mô hình có thể áp dụng |
| Paradigm Shift | Thay đổi tư duy, góc nhìn mới, phản bác niềm tin cũ |
| Bài học thực tế / Case study | Ví dụ cụ thể, kết quả thật, con số |
| Cảnh báo / Sai lầm phổ biến | Lỗi thường gặp, cái bẫy, rủi ro |
| Step-by-step / Hướng dẫn | Quy trình rõ ràng, làm theo được ngay |
| Số liệu / So sánh | Con số wow, before/after, benchmark |

**Rules:**
- Mỗi nugget cần: **loại**, **tiêu đề** (1 dòng), **mô tả** (1-2 câu)
- Tối đa 8 nuggets - chỉ giữ những cái có giá trị thật
- Bỏ qua filler, intro, CTA, sponsor segments

### Bước 3: Đánh giá tiềm năng làm Facebook Content

Chấm điểm từ 1-10 cho mỗi tiêu chí:

| Tiêu chí | Điểm (1-10) | Ghi chú |
|----------|-------------|---------|
| Độ liên quan với audience Facebook | | Audience = người quan tâm AI, tech, automation, solopreneur |
| Tính "chia sẻ được" (shareability) | | Có insight gây "à ha" không? Có controversial không? |
| Tính hành động (actionable) | | Người đọc có thể làm theo ngay không? |
| Dễ hiểu với non-tech | | Người không rành tech có hiểu không? |
| Tính thời sự / trending | | Có đang hot không? Có FOMO không? |
| **TỔNG ĐIỂM TRUNG BÌNH** | | /10 |

**Phân loại:**
- 8-10: XANH -- Rất phù hợp — nên làm content ngay
- 5-7: VÀNG -- Khá phù hợp — cần chọn góc kể tốt
- 1-4: ĐỎ -- Ít phù hợp — bỏ qua hoặc chỉ dùng 1 insight nhỏ

**Nếu tổng điểm ĐỎ (1-4): DỪNG tại Bước 3. Nói thẳng lý do video không phù hợp. KHÔNG làm Bước 4 và Bước 5. Không ép ra content.**

**Chỉ tiếp tục Bước 4 + 5 khi tổng điểm XANH (8-10) hoặc VÀNG (5-7).**

### Bước 4: Gợi ý Format Content (chỉ khi XANH hoặc VÀNG)

Với mỗi knowledge nugget có tiềm năng, gợi ý format phù hợp nhất:

**Format 1: Bài viết Facebook (Text + Hình)**
- Phù hợp khi: Có framework, so sánh, danh sách, thay đổi tư duy
- Cấu trúc: Hook > Vấn đề > Nội dung chính > CTA

**Format 2: Short Video / Reels (30-90 giây)**
- Phù hợp khi: Có demo, step-by-step, before/after, số liệu wow
- Cấu trúc: Hook 3s > Vấn đề > Giải pháp (3 bước) > CTA
- **Tạo hook:** Dùng skill `mkt-desire-hook-for-video`
- **Tạo kịch bản:** Dùng skill `mkt-create-script-short-video`

**Format 3: Actionable Post (Tutorial step-by-step)**
- Phù hợp khi: Có quy trình rõ ràng, người đọc làm theo được ngay
- Cấu trúc: Vấn đề > Từng bước cụ thể > Kết quả kỳ vọng > CTA

**Format 4: Hình ảnh Infographic / Carousel**
- Phù hợp khi: Có bảng so sánh, pyramid, timeline, danh sách
- Cấu trúc: Slide 1 (hook) > Slide 2-5 (nội dung) > Slide cuối (CTA)

### Bước 5: Sơ bộ nội dung Draft (chỉ khi XANH hoặc VÀNG)

Với mỗi gợi ý content, viết sơ bộ theo format tương ứng:

#### Nếu là Bài viết Facebook:
- **Hook (dòng đầu tiên):** Viết hook gây tò mò, dưới 2 dòng
- **Body:** 3-5 đoạn ngắn, mỗi đoạn 2-3 câu
- **CTA:** Câu kêu gọi tương tác: comment, save, share
- **Gợi ý hình ảnh đi kèm:** Mô tả hình cần thiết kế

#### Nếu là Short Video / Reels:
**KHÔNG tự viết hook và kịch bản. Gọi 2 skill chuyên dụng:**
1. Gọi skill `mkt-desire-hook-for-video` để tạo hook -- truyền chủ đề + đối tượng từ phân tích
2. Gọi skill `mkt-create-script-short-video` để tạo kịch bản đầy đủ -- truyền nugget content + hook đã tạo

#### Nếu là Actionable Post:
- **Hook:** Dòng đầu gây pain point
- **Các bước:** Bước 1 > Bước 2 > ... (mỗi bước 2-3 câu)
- **Kết quả kỳ vọng:** Người đọc đạt được gì sau khi làm theo
- **CTA:** Kêu gọi thử và phản hồi

#### Nếu là Infographic / Carousel:
- **Slide 1 - Hook:** Tiêu đề gây tò mò
- **Slide 2-5 - Nội dung:** Mỗi slide 1 ý chính
- **Slide cuối - CTA:** Kêu gọi follow/save/share

---

## Output Format

```
=======================================
PHÂN TÍCH VIDEO
=======================================

Video: [Tiêu đề video]
Views: [Số view nếu có]

--- TÓM TẮT ---
[3-5 câu tóm tắt]

--- KNOWLEDGE NUGGETS ---
1. [Loại] - [Tiêu đề]
   [Mô tả 1-2 câu]

2. [Loại] - [Tiêu đề]
   [Mô tả 1-2 câu]
...

--- ĐÁNH GIÁ TIỀM NĂNG ---

| Tiêu chí | Điểm | Ghi chú |
|----------|------|---------|
| Độ liên quan audience | X/10 | ... |
| Shareability | X/10 | ... |
| Actionable | X/10 | ... |
| Dễ hiểu non-tech | X/10 | ... |
| Trending/thời sự | X/10 | ... |
| TỔNG ĐIỂM | X/10 | [XANH/VÀNG/ĐỎ] |

--- GỢI Ý CONTENT ---

=======================================
CONTENT #1: [Tên / Góc khai thác]
Format: [Facebook Post / Reels / Actionable / Infographic]
Nugget gốc: #[số]
=======================================

[Draft nội dung đầy đủ -- TIẾNG VIỆT CÓ DẤU]

---

=======================================
CONTENT #2: [Tên / Góc khai thác]
Format: [Facebook Post / Reels / Actionable / Infographic]
Nugget gốc: #[số]
=======================================

[Draft nội dung đầy đủ -- TIẾNG VIỆT CÓ DẤU]
```

---

## Mandatory Rules

### Ngôn ngữ
- **TUYỆT ĐỐI phải viết tiếng Việt CÓ DẤU đầy đủ** trong toàn bộ output (tóm tắt, nuggets, đánh giá, draft bài viết)
- **Viết cực kỳ đơn giản** -- học sinh lớp 5 đọc cũng hiểu. Không dùng từ khó, không viết câu dài.
- Thuật ngữ tiếng Anh phải giải thích bằng tiếng Việt ngay sau. Ví dụ: "Framework (khung quy trình)", "Shareability (khả năng chia sẻ)"
- Dùng ví dụ so sánh đời thường để giải thích khái niệm phức tạp

### Phân tích
- Đọc TOÀN BỘ transcript - không bỏ sót
- Trích xuất insight chính xác từ nội dung - không bịa
- Đánh giá trung thực - nếu video ít giá trị thì nói thẳng
- Mỗi video gợi ý 1-3 content pieces, không ép ra nhiều

### Viết draft
- **PHẢI** đọc và áp dụng brand voice từ BRANDVOICE.MD
- Hook phải tạo được "gap" hoặc "shock" trong 2 dòng đầu
- KHÔNG dùng emoji, icon, ký tự đặc biệt trong draft bài viết
- Giọng văn: thân thiện, thực tế, không hàn lâm, như đang nói chuyện với bạn bè
- Mỗi bài viết Facebook không quá 300 từ
- Mỗi kịch bản Reels không quá 90 giây
- Luôn kết thúc bằng CTA rõ ràng
- Có số liệu cụ thể nếu transcript cung cấp

### Output
- Draft phải copy-paste ready
- Lưu output vào `workspace/content/ideas/` nếu user yêu cầu save
- Tên file: `[slug-tiêu-đề]-content-ideas.md`

---

## Example

**Input:**
- Tiêu đề: "How to Use Claude Code Better Than 99% of People"
- Transcript: [nội dung transcript]
- Insight: Framework — CLAUDE.md là "bộ nhớ dài hạn" của Claude Code
- Views: 21,598

**Output mẫu (trích đoạn draft):**

```
Bạn đang dùng AI như một chatbot.
Nhưng những người hiểu chuyện đang đối xử với nó như một nhân viên mới.

Nghe có vẻ giống nhau? Khác hoàn toàn.

Khi bạn dùng AI như chatbot, mỗi lần mở lên bạn phải giải thích lại từ đầu:
bạn là ai, công ty làm gì, mục tiêu là gì. AI trả lời xong, quên sạch.

Nhưng khi bạn "onboard" AI -- giống như đào tạo nhân viên mới -- bạn chỉ cần
làm một lần. Cho nó đọc sổ tay công ty, cho nó biết mục tiêu của bạn.
Từ đó, nó tự hiểu và làm việc tốt hơn mỗi ngày.

System đúng -- một người làm bằng mười.

Bạn đã "onboard" AI chưa? Comment cho mình biết.
```
