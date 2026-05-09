---
name: mkt-topic-to-video-ideas
description: End-to-end pipeline — research YouTube videos by topic, analyze via NotebookLM, and generate short video ideas for TikTok/Facebook. USE WHEN user says 'research topic rồi đề xuất video', 'tìm video theo chủ đề rồi phân tích', 'research topic to video ideas', 'từ chủ đề ra ý tưởng video ngắn', 'topic research pipeline', 'phân tích chủ đề youtube rồi gợi ý content', 'nghiên cứu chủ đề rồi đề xuất video tiktok', 'research và đề xuất video ngắn', 'youtube topic to content ideas', 'từ keyword ra video ideas'.
---

# Topic → Research → Video Ideas Pipeline

Pipeline 3 giai đoạn: từ một chủ đề/keyword → tìm video YouTube thành công → phân tích insight qua NotebookLM → đề xuất ý tưởng video ngắn cho TikTok/Facebook.

Skill này kết hợp 3 công cụ: `mkt-youtube-topic-researcher` (tìm video), NotebookLM MCP (phân tích AI), và brand voice Hoàng (đề xuất content).

---

## When to Use

- User có một chủ đề và muốn tìm hiểu video nào đang hot, rồi từ đó nghĩ ra ý tưởng video ngắn
- User muốn pipeline tự động: keyword → research → insight → content ideas
- User muốn phân tích nhiều video cùng lúc qua NotebookLM thay vì đọc từng cái

---

## Input

User cung cấp:
- **Chủ đề / keyword** (bắt buộc) — vd: "AI agents", "claude code", "automation"
- **Số lượng video** (tùy chọn, mặc định 30)
- **Min views** (tùy chọn, mặc định 10,000)
- **Date range** (tùy chọn, mặc định month)

---

## Phase 1: RESEARCH — Tìm video YouTube

Chạy script `mkt-youtube-topic-researcher` để tìm video theo chủ đề.

```bash
uv run .claude/skills/mkt-youtube-topic-researcher/scripts/research_topic.py "KEYWORD" \
  --max-results 30 \
  --min-views 10000 \
  --date month \
  --sort views
```

**Output:** File `research/youtube/topics/[slug]/videos.json` chứa danh sách video kèm metadata (views, subs, breakout ratio).

Trình bày bảng kết quả cho user xem. Hỏi user:
- Có muốn điều chỉnh filters không? (tăng/giảm min-views, đổi date range)
- Có muốn loại bỏ video nào không?
- Sẵn sàng tiến sang phân tích chưa?

Chờ user xác nhận trước khi qua Phase 2.

---

## Phase 2: ANALYZE — Phân tích qua NotebookLM

### Bước 2.1: Tạo hoặc dùng notebook

Thử tạo notebook mới trước:

```
notebook_create(title="Research: [KEYWORD] - [DATE]")
```

Nếu `notebook_create` thất bại (lỗi API hiện tại), dùng notebook xử lý sẵn có:
- Notebook ID: `d74a5dac-b88b-4b09-b488-bbf2c1d5d649`
- Trước khi dùng, xóa hết sources cũ bằng `source_delete`

### Bước 2.2: Thêm video vào NotebookLM

Thêm từng video URL vào notebook. NotebookLM sẽ tự fetch transcript và index nội dung.

```
source_add(notebook_id=NOTEBOOK_ID, source_type="url", url="https://youtube.com/watch?v=VIDEO_ID", wait=True)
```

**Lưu ý quan trọng:**
- Thêm **tối đa 15-20 video** (NotebookLM có giới hạn sources, và một số video có thể không có transcript)
- Ưu tiên thêm video có **breakout ratio cao nhất** hoặc **views cao nhất** — đây là video đáng phân tích nhất
- Nếu source_add thất bại cho video nào, bỏ qua và tiếp tục video kế tiếp
- Thông báo cho user tiến trình: "Đang thêm video 5/15..."

### Bước 2.3: Phân tích insights

Sau khi thêm xong sources, query notebook để lấy insights tổng hợp:

**Query 1 — Tổng quan chủ đề:**
```
notebook_query(notebook_id, query="Phân tích tổng quan: Các video này nói về chủ đề gì chung? Có những góc tiếp cận (angles) nào khác nhau? Liệt kê 5-7 angles phổ biến nhất.")
```

**Query 2 — Patterns thành công:**
```
notebook_query(notebook_id, query="Phân tích patterns: Những video nào có cách tiếp cận hấp dẫn nhất? Title patterns nào được dùng nhiều? Hook mở đầu có đặc điểm gì chung? Liệt kê 5 patterns nổi bật nhất.")
```

**Query 3 — Insights độc đáo:**
```
notebook_query(notebook_id, query="Tìm 5-10 insights hay nhất, bất ngờ nhất, hoặc gây tranh cãi nhất từ các video. Mỗi insight ghi: nội dung + video nguồn + lý do nó hay.")
```

**Query 4 — Gaps và cơ hội:**
```
notebook_query(notebook_id, query="Có chủ đề phụ nào chưa được cover kỹ? Có góc nhìn nào bị thiếu? Có sai lầm phổ biến nào mà nhiều video mắc phải? Đây là cơ hội content.")
```

Trình bày kết quả phân tích cho user. Hỏi user có muốn hỏi thêm gì từ notebook không.

---

## Phase 3: IDEAS — Đề xuất ý tưởng video ngắn

Dựa trên insights từ Phase 2, đề xuất **8-10 ý tưởng video ngắn** phù hợp đăng TikTok và Facebook.

### Format đề xuất

Mỗi ý tưởng trình bày theo template này:

```
### Ý tưởng #[N]: [Tiêu đề gợi ý]

**Góc tiếp cận:** [Angle — vd: myth-busting, before-after, listicle, reaction]
**Nguồn insight:** [Video/insight nào gợi cảm hứng]
**Platform:** TikTok / Facebook / Cả hai

**Hook gợi ý (3 giây đầu):**
"[Câu hook — phải gây tò mò, có số cụ thể nếu được]"

**Nội dung chính (30-60 giây):**
- Điểm 1: ...
- Điểm 2: ...
- Điểm 3: ...

**CTA:**
[Kêu gọi hành động — follow, comment, chia sẻ, hoặc link cộng đồng AI Freedom Builders]

**Độ khó sản xuất:** Dễ / Trung bình / Khó
**Loại visual:** Talking head / Screen recording / Text overlay / Mix
```

### Tiêu chí chọn ý tưởng

Ý tưởng tốt cần thỏa mãn:

1. **Dựa trên insight thực** — không bịa, phải trỏ được về video/data nguồn
2. **Phù hợp brand voice Hoàng** — chuyên gia AI, One Person Business, 7/10 energy
3. **Đa dạng angles** — mix giữa listicle, myth-busting, before-after, reaction, tutorial
4. **Có yếu tố viral** — gây tranh cãi nhẹ, bất ngờ, hoặc counter-intuitive
5. **Sản xuất được ngay** — ưu tiên ý tưởng dễ quay/edit, không cần quá nhiều b-roll
6. **Phù hợp target audience** — Vietnamese SME owners, managers, 28-45 tuổi

### Phân loại theo platform

- **TikTok:** 30-60 giây, pace nhanh, hook cực mạnh, nhiều text overlay
- **Facebook:** 60-90 giây, pace vừa phải, chia sẻ kiến thức sâu hơn, kêu gọi comment/share

---

## Output

### Files lưu lại

Tất cả output lưu vào `research/youtube/topics/[slug]/`:

| File | Nội dung |
|------|----------|
| `videos.json` | Danh sách video từ Phase 1 (auto-saved bởi script) |
| `analysis.md` | Tổng hợp insights từ Phase 2 |
| `video-ideas.md` | Danh sách 8-10 ý tưởng video ngắn từ Phase 3 |

### Template `analysis.md`

```markdown
# Topic Research Analysis: "[KEYWORD]"
**Date:** [DATE]
**Videos analyzed:** [N] / [TOTAL found]
**NotebookLM Notebook:** [NOTEBOOK_ID or link]

## Tổng quan chủ đề
[Summary từ Query 1]

## Patterns thành công
[Summary từ Query 2]

## Top Insights
[Summary từ Query 3]

## Gaps & Cơ hội
[Summary từ Query 4]
```

### Template `video-ideas.md`

```markdown
# Video Ideas: "[KEYWORD]"
**Date:** [DATE]
**Dựa trên:** [N] videos phân tích
**Platform:** TikTok + Facebook

## Ý tưởng #1: [Title]
...

## Ý tưởng #2: [Title]
...
```

---

## User Approval Gates

Skill này có 3 điểm dừng để user xác nhận:

| Gate | Sau phase | Hỏi user |
|------|-----------|----------|
| **Gate 1** | Phase 1 (Research) | "Kết quả tìm được [N] video. Muốn điều chỉnh gì không?" |
| **Gate 2** | Phase 2 (Analyze) | "Đã phân tích xong. Muốn hỏi thêm gì từ NotebookLM không?" |
| **Gate 3** | Phase 3 (Ideas) | "Đây là [N] ý tưởng. Muốn phát triển ý nào thành script?" |

Sau Gate 3, nếu user chọn một ý tưởng, có thể chuyển tiếp sang skill `mkt-create-script-short-video` hoặc `mkt-create-script-short-video-v2-vn` để viết kịch bản chi tiết.

---

## Troubleshooting

| Vấn đề | Giải pháp |
|--------|-----------|
| Script research không tìm thấy video | Hạ min-views, mở rộng date range, thử keyword khác |
| NotebookLM source_add thất bại | Video có thể không có transcript công khai. Bỏ qua, thêm video khác |
| NotebookLM notebook_create thất bại | Dùng notebook xử lý sẵn có (ID trong config) |
| Query trả về kết quả chung chung | Thử query cụ thể hơn, hoặc giảm số sources để tập trung |
| Quá nhiều video (>20) cho NotebookLM | Chỉ thêm top 15 video theo breakout ratio / views |

---

## Ví dụ sử dụng

```
User: "Research chủ đề AI agents rồi đề xuất video ngắn cho tiktok"
→ Phase 1: Tìm 30 video "AI agents", min 10K views, tháng này
→ Phase 2: Thêm top 15 video vào NotebookLM, phân tích insights
→ Phase 3: Đề xuất 8-10 ý tưởng video ngắn

User: "Tìm video về vibe coding, trên 50K views, rồi gợi ý content"
→ Phase 1: Tìm 30 video "vibe coding" --min-views 50000
→ Phase 2: Phân tích qua NotebookLM
→ Phase 3: Đề xuất ý tưởng phù hợp TikTok + Facebook
```
