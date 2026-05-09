---
name: mkt-xpost-to-facebook-knowledge
description: Chuyển X posts (tweets) về AI/tech thành bài Facebook chia sẻ kiến thức theo brand voice Hoàng. USE WHEN user says 'chuyển tweet thành facebook', 'viết facebook từ X post', 'X post to facebook', 'tweet to facebook', 'repurpose X post', 'repurpose tweet', 'viết bài facebook từ tweet', 'chuyển post X thành content', hoặc khi input là nội dung từ X.com/Twitter cần biến thành bài Facebook. Cũng áp dụng khi user cung cấp link X post hoặc nội dung tweet kèm yêu cầu tạo Facebook content.
---

# X Post to Facebook Knowledge-Sharing Content

Biến X posts (tweets, threads) về AI, tools, GitHub repos thành bài Facebook chia sẻ kiến thức — viết cho người muốn ỨNG DỤNG AI, không phải lập trình viên.

## Brand Voice

Đọc [BRANDVOICE.MD](../../../MY RESOURCES/BRANDVOICE.MD) trước khi viết.

**Tóm tắt nhanh:**
- Xưng hô: "Hoàng" / "mình", gọi "bạn" / "các bạn"
- Giọng: Conversational expert, 7/10 energy — tự tin, sắc bén, truyền cảm hứng hành động
- Nhịp điệu: Mix câu ngắn, trung bình, dài — không đều đều
- Power words giữ tiếng Anh: System, Automation, AI, Framework, Workflow, Template, Scale
- Luôn hướng đến kết quả đo được: tiết kiệm thời gian, giảm chi phí, tăng hiệu suất

## Tư duy cốt lõi — Tại sao skill này tồn tại

X posts thường ngắn, technical, viết cho developer audience. Audience Facebook của Hoàng là chủ doanh nghiệp, solopreneur, office workers (28-45) — họ muốn biết **AI giúp gì cho công việc của họ**, không muốn đọc code hay kiến trúc hệ thống.

Nhiệm vụ của skill này là **dịch** từ ngôn ngữ developer sang ngôn ngữ người dùng: tool này giải quyết vấn đề gì, tiết kiệm bao nhiêu thời gian, thay thế công việc thủ công nào. X post là nguồn tin — Facebook post là bài chia sẻ kiến thức từ Hoàng.

## Input

Mỗi lần gọi skill, cần ít nhất:

1. **X post content** — Nội dung tweet/thread (text)
2. **Source URL** (optional nhưng khuyến khích) — Link GitHub repo, article, tool page được đề cập trong tweet

Nếu có source URL (đặc biệt GitHub repo), **BẮT BUỘC** đọc source trước khi viết. Lý do: X posts thường tóm tắt quá ngắn hoặc hype quá mức — cần verify từ source gốc để viết chính xác.

Nếu user cung cấp nhiều X posts cùng lúc, xử lý từng post và tạo 1-2 bài Facebook cho mỗi post phù hợp.

## Workflow

### Phase 1: Phân tích X post + Source

**Bước 1 — Đọc X post:**
- Nội dung chính tweet/thread nói gì?
- Có số liệu cụ thể không? (stars, users, downloads, performance metrics)
- Ai là tác giả? Có credibility gì đặc biệt?
- Tool/repo/concept nào được đề cập?

**Bước 2 — Verify từ source (nếu có URL):**
- Đọc GitHub README, article, hoặc tool page
- Trích xuất: tool làm gì, dùng cho ai, giải quyết vấn đề gì
- Lấy số liệu thực: stars, contributors, features chính
- Xác nhận hoặc bác bỏ các claim trong X post
- **KHÔNG bịa số liệu** — chỉ dùng data có thể verify

**Bước 3 — Xác định góc viết (lens):**
Chọn 1-2 góc phù hợp nhất từ danh sách:

| Góc viết | Khi nào dùng | Ví dụ |
|----------|-------------|-------|
| **Tiết kiệm thời gian** | Tool/workflow thay thế công việc thủ công | "Tool này thay 3 giờ tìm việc mỗi ngày bằng 5 phút" |
| **One Person Power** | 1 người làm được việc cả team nhờ AI | "1 người + tool này = team marketing 5 người" |
| **Xu hướng AI** | Tin tức, trend mới, milestone quan trọng | "Claude vừa làm điều mà 6 tháng trước còn không tưởng" |
| **Bài học rút ra** | Insight sâu từ case study, kinh nghiệm | "Điều mình học được từ cách anh này dùng AI..." |
| **So sánh & lựa chọn** | A vs B, trước/sau, cũ vs mới | "Trước dùng 3 tool, giờ chỉ cần 1" |
| **Ứng dụng thực tế** | Demo, hướng dẫn cách dùng cho non-dev | "Bạn không cần biết code để dùng tool này" |

### Phase 2: Viết bài Facebook

Chọn format phù hợp từ [Post Templates](references/post_templates.md) và viết theo.

**Quy tắc viết TUYỆT ĐỐI:**

1. **Giọng chia sẻ kiến thức, KHÔNG phải tin tức**
   - Đúng: "Mình vừa đọc được một case study hay..."
   - Đúng: "Hôm qua lướt X thấy một tool mà phải chia sẻ ngay..."
   - Đúng: "Bài học ở đây là..."
   - Sai: "Theo nguồn tin từ X.com..."
   - Sai: "Mới đây, developer Santiago đã công bố..."

2. **Viết cho người DÙNG AI, không phải developer**
   - Đúng: "Tool này tự động scan 700+ vị trí, lọc phù hợp, và tạo CV riêng cho từng job"
   - Sai: "Tool viết bằng Go, dùng Playwright cho browser automation, kiến trúc chia thành 3 modules"
   - Đúng: "Kết quả: tiết kiệm 3 giờ mỗi ngày tìm việc"
   - Sai: "Repository có 15 stars, sử dụng Claude API với structured output"

3. **KHÔNG đặt URL trong thân bài**
   - Khi cần share link (repo, tool, khóa học): dùng CTA kiểu "Link ở comments nhé các bạn" hoặc "Comments mình gửi link nhé"
   - KHÔNG BAO GIỜ viết: "github.com/...", "tranvanhoang.com/...", hay bất kỳ URL nào trong body

4. **KHÔNG dùng emoji, icon, ký tự đặc biệt**
   - Chỉ dùng text thuần, dấu gạch ngang (-), dấu chấm, dấu phẩy, dấu hai chấm
   - KHÔNG: ✅, ❌, 🔴, →, •, 1️⃣, hay bất kỳ Unicode đặc biệt nào

5. **Hook 2 dòng đầu phải tạo gap hoặc shock**
   - KHÔNG mở đầu kiểu "Hôm nay mình chia sẻ..."
   - Đi thẳng vào insight gây tò mò

6. **Cấu trúc The Dance**: Hook > Bối cảnh > Nhưng (xung đột) > Vì vậy (giải pháp) > Last Dab + CTA

7. **300-600 từ mỗi bài** — đủ sâu nhưng không quá dài

8. **Chỉ viết những gì verify được** — nếu X post claim điều gì mà source không confirm, bỏ claim đó ra

### Phase 3: Review checklist

Trước khi output, kiểm tra từng bài qua checklist:

- [ ] Có URL nào trong thân bài không? → Xóa, chuyển sang CTA comments
- [ ] Có emoji/icon không? → Xóa
- [ ] Có thuật ngữ lập trình không? (kiến trúc, module, API call, repository structure) → Viết lại bằng ngôn ngữ user benefit
- [ ] Hook có gây tò mò không? → Nếu nhạt, viết lại
- [ ] Có số liệu cụ thể không? → Nếu có data, phải dùng
- [ ] Giọng có đang "báo cáo tin tức" không? → Chuyển sang "chia sẻ kiến thức"
- [ ] CTA có phù hợp không? → Link share qua comments, không trong body

## Output Format

```
═══════════════════════════════════════
PHÂN TÍCH X POST
═══════════════════════════════════════

Source: [X post author — @handle]
Content: [Tóm tắt 1-2 dòng nội dung X post]
Source URL: [Link nếu có, hoặc "Không có"]
Verified data: [Những gì đã verify từ source gốc]
Góc viết đã chọn: [Tên góc]

═══════════════════════════════════════
BÀI VIẾT #1: [Tên / Góc khai thác]
Format: [Actionable / Comparison / Listicle / Deep-dive]
═══════════════════════════════════════

[Nội dung bài viết Facebook — copy-paste ready]

---

═══════════════════════════════════════
BÀI VIẾT #2: [Tên / Góc khai thác] (nếu có)
Format: [Actionable / Comparison / Listicle / Deep-dive]
═══════════════════════════════════════

[Nội dung bài viết Facebook — copy-paste ready]
```

## Rules tóm tắt

1. **Verify trước khi viết** — đọc source URL nếu có, không viết từ X post summary alone
2. **Viết cho người dùng AI** — user benefit, business outcome, tiết kiệm thời gian — KHÔNG code architecture
3. **Giọng chia sẻ kiến thức** — "mình đọc được", "bài học là", "mình thấy hay ở chỗ" — KHÔNG tin tức
4. **URL ở comments** — không bao giờ đặt link trong thân bài Facebook
5. **Không emoji** — text thuần, dấu gạch ngang, dấu chấm
6. **Không bịa data** — chỉ dùng số liệu verify được
7. **1-2 bài mỗi X post** — mỗi bài một góc nhìn khác nhau
8. **Copy-paste ready** — output không cần chỉnh sửa thêm
