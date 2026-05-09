---
name: mkt-xcom-post-creator
description: Create X.com (Twitter) threads and standalone posts in ENGLISH from transcript, insight, or topic. Auto-detect content type and choose best format. Output in English with Hoàng's brand voice. USE WHEN user says 'tạo post X', 'viết thread twitter', 'X.com post', 'tạo tweet', 'twitter thread', 'viết cho X', 'post X.com'.
---

# X.com Post Creator

Create threads and standalone posts for X.com in **ENGLISH** from transcript/insight/topic. Optimized for X.com algorithm and global tech community audience.

## Content Language Rule

**X.com content MUST be written in English.** Only Facebook and YouTube use Vietnamese. LinkedIn, X.com, and Instagram all use English for global reach.

## Brand Voice Reference

- [BRANDVOICE.MD](../../../MY RESOURCES/BRANDVOICE.MD) - DNA Brand Voice Hoàng (adapt to English)

**Brand voice adapted for X.com (English):**
- Voice: "I" / "Hoang", address readers: "you"
- Tone: Sharper than Facebook — authority voice, data-driven, punchy
- Energy: 8/10 — higher than Facebook, sharper, bolder
- Power words: System, Automation, AI, Framework, Workflow, Template, Scale, ROI
- Tech terms used freely (X.com audience is tech-native)
- NO emoji in body text
- Always include specific data points

## Platform Rules — X.com

| Rule | Detail |
|------|--------|
| Character limit | 280 chars/tweet (Vietnamese ~200 chars để safe) |
| Hook tweet | PHẢI standalone — hiện trên timeline không cần mở thread |
| Hashtags | Max 3, chỉ ở tweet cuối hoặc standalone posts |
| Links | Chỉ ở tweet cuối (X deprioritize linked tweets) |
| Tone | Sharper, data-driven, authority — ít conversational hơn FB |
| Thread length | 3-10 tweets tùy format |
| Line breaks | Tối đa 1 line break giữa các ý trong 1 tweet |

## Workflow

### Phase 1: Thu thập thông tin

Khi user gọi skill, cần ít nhất 1 input:

1. **Transcript** — Nội dung transcript video (ưu tiên)
2. **Topic + Insight** — Chủ đề + insight cụ thể
3. **Bài viết Facebook** — Adapt từ bài FB có sẵn sang X.com format

Nếu thiếu, hỏi user trước khi tiếp tục.

### Phase 2: Phân tích & chọn format

Đọc input và phân tích:

**Bước 1 — Nhận diện loại nội dung:**

| Loại | Dấu hiệu | Best Format |
|------|-----------|-------------|
| How-to, steps, tips | Liệt kê bước, hướng dẫn | Step-by-step Thread |
| Data, research, trends | Số liệu, stats, nghiên cứu | Insight Thread |
| Opinions, hot takes | Quan điểm mạnh, counter-intuitive | Hot Take Thread |
| Tools, resources list | Danh sách tools/resources | Tool/Resource Thread |
| Single powerful insight | 1 câu nói mạnh, quote | Standalone Post |

**Bước 2 — Trích xuất key points:**
- Main argument / thesis
- Supporting data points (số liệu, stats)
- Counter-intuitive angle
- Actionable takeaway
- CTA destination

**Bước 3 — Chọn output format:**
- Nếu content đủ sâu: Thread (3-10 tweets)
- Nếu content ngắn gọn: 1-2 Standalone posts
- Có thể output cả thread + standalone nếu content phong phú

### Phase 3: Tạo content

Dựa trên phân tích, tạo content theo templates trong [Thread Templates](references/thread-templates.md) và [Post Templates](references/post-templates.md).

**Quy tắc viết bắt buộc:**
1. Hook tweet phải gây shock/tò mò trong 280 chars — quyết định người đọc có mở thread không
2. Mỗi tweet phải có giá trị standalone — không viết "Tiếp theo..." hay "Như đã nói..."
3. KHÔNG dùng emoji, icon, ký tự đặc biệt trong body
4. Hashtags chỉ ở tweet cuối, max 3 hashtags
5. Link chỉ đặt ở tweet cuối
6. Mỗi tweet dưới 280 ký tự (đếm kỹ cho tiếng Việt có dấu)
7. Thread bookmark tweet cuối: tóm tắt + CTA

## Output Format

```
═══════════════════════════════════════
PHAN TICH INPUT
═══════════════════════════════════════

Source: [Tiêu đề / chủ đề]
Loại nội dung: [How-to / Data / Opinion / Tools / Single Insight]
Format chọn: [Thread type / Standalone]

Key Points:
1. [Point 1]
2. [Point 2]
3. [Point 3]

═══════════════════════════════════════
THREAD: [Tiêu đề thread]
Format: [Insight / Step-by-step / Hot Take / Tool-Resource]
Số tweets: [N]
═══════════════════════════════════════

Tweet 1/N (Hook):
[Nội dung tweet — max 280 chars]

---

Tweet 2/N:
[Nội dung tweet]

---

...

Tweet N/N (CTA):
[Nội dung tweet + hashtags + link]

═══════════════════════════════════════
STANDALONE POST (nếu có)
═══════════════════════════════════════

[Nội dung standalone post — max 280 chars]
```

## Mandatory Rules

### Phân tích
- Đọc TOÀN BỘ input — không bỏ sót
- Trích xuất insight chính xác — không bịa
- Đếm ký tự mỗi tweet — KHÔNG vượt 280

### Viết
- **PHẢI** đọc và áp dụng brand voice từ BRANDVOICE.MD
- Hook tweet phải work standalone trên timeline
- Mỗi tweet có giá trị riêng — đọc riêng vẫn hiểu
- Tone sắc bén, authority — không dài dòng
- Dùng số liệu cụ thể nếu có
- Vietnamese có dấu đầy đủ, giữ English tech terms

### Output
- Content phải copy-paste ready
- Lưu output vào `workspace/content/xcom/` nếu user yêu cầu save
- Tên file: `[slug]-xcom-posts.md`

## Example

**Input:**
- Topic: Claude Code Agent Teams
- Insight: Agent Teams cho phép nhiều agent giao tiếp với nhau, khác Sub Agents chỉ chạy parallel không nói chuyện

**Output:**

Thread format: Hot Take (5 tweets)

Tweet 1/5 (Hook):
Sub Agent và Agent Team KHÔNG phải upgrade của nhau.

Đó là 2 cách tư duy hoàn toàn khác về AI coding.

95% dev đang chọn sai.

Tweet 2/5:
Sub Agent = giao việc parallel. Nhanh, hiệu quả, nhưng mỗi agent là một ốc đảo.

Agent A không biết Agent B đang làm gì. Conflict? Duplicate? Tự xử.

Tweet 3/5:
Agent Team = một đội thực sự. Agents giao tiếp, chia sẻ context, phối hợp real-time.

Agent A viết API, Agent B viết tests — cả hai biết schema của nhau.

Kết quả: code consistent, ít bugs hơn 3x.

Tweet 4/5:
Khi nào dùng gì?

Sub Agent: tasks độc lập, không cần sync. VD: format 10 files cùng lúc.

Agent Team: tasks phụ thuộc nhau, cần coordination. VD: build full feature end-to-end.

Tweet 5/5:
Một người + đúng AI system = output như team 5 dev.

Không phải tools — mà là cách bạn orchestrate chúng.

Mình chia sẻ setup chi tiết tại đây: [link]

#ClaudeCode #AICoding #AIAutomation
