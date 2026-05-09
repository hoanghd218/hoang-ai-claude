---
name: mkt-xcom-viral-knowledge-finder
description: Tìm các bài đăng viral trên X.com (Twitter) về Claude.ai và các chủ đề AI đang hot — tập trung vào dạng bài CHIA SẺ KIẾN THỨC (threads, tips, tutorials, frameworks, how-tos) thay vì hype/news. Dùng Grok model qua OpenRouter API để search và lọc. USE WHEN user says 'tìm bài viral claude', 'viral x post claude', 'find viral x posts about AI', 'tìm thread AI hay', 'x.com knowledge posts', 'tìm post chia sẻ kiến thức claude', 'viral tweet AI', 'tweet AI hot', 'thread claude ai viral', 'x trending claude', 'grok search x posts', 'knowledge tweet', 'AI thread trending', 'viral knowledge x'.
---

# X.com Viral Knowledge Finder (Claude.ai / AI Topics)

Tìm top viral posts trên X.com mang tính **chia sẻ kiến thức** (thread, tips, frameworks, tutorials, workflow) về Claude.ai hoặc các chủ đề AI đang hot. Dùng **Grok via OpenRouter** (không phải xAI API trực tiếp) để research.

Phân biệt với skill khác:
- `mkt-ai-news-aggregator/search_x_posts.py` — news/trending tổng hợp, dùng xAI API trực tiếp
- Skill này — chỉ knowledge-sharing, ưu tiên threads dài, tutorial, tips có value để repurpose thành content

---

## When to Use

- User muốn tìm thread X.com hay về Claude.ai để học/repurpose
- Cần seed content cho Pillar 1 (AI Demo/Tutorial) từ nguồn X
- Tìm góc nhìn mới về AI agent, prompt engineering, workflow
- Research trước khi viết script/post về 1 chủ đề AI

Không dùng khi:
- Chỉ cần tin tức nhanh → dùng `mkt-ai-news-aggregator`
- Cần data chuyên về repo/tool → dùng `github-trend-finder`

---

## Prerequisites

`.env` cần có:
```
OPENROUTER_API_KEY=sk-or-...
```

Dependency: `requests`, `python-dotenv` (auto-install qua `uv run`).

---

## Usage

```bash
# Default: Claude.ai knowledge posts last 7 days, top 10
uv run .claude/skills/mkt-xcom-viral-knowledge-finder/scripts/search_x_viral_knowledge.py

# Topic tùy biến
uv run .claude/skills/mkt-xcom-viral-knowledge-finder/scripts/search_x_viral_knowledge.py \
    --topic "claude code agent" --period week --limit 15

# Chọn model Grok khác qua OpenRouter
uv run .claude/skills/mkt-xcom-viral-knowledge-finder/scripts/search_x_viral_knowledge.py \
    --topic "AI agent frameworks" --model "x-ai/grok-4"

# Output text thay vì JSON
uv run .claude/skills/mkt-xcom-viral-knowledge-finder/scripts/search_x_viral_knowledge.py \
    --topic "prompt engineering" --format text

# Không lưu file, chỉ in stdout
uv run .claude/skills/mkt-xcom-viral-knowledge-finder/scripts/search_x_viral_knowledge.py --no-save
```

### Options

| Flag | Default | Mô tả |
|------|---------|-------|
| `--topic` | `Claude.ai` | Chủ đề cần tìm (e.g. "claude code", "AI agent", "prompt engineering") |
| `--period` | `week` | `24h` \| `week` \| `month` |
| `--limit` | `10` | Số post tối đa |
| `--model` | `x-ai/grok-4-fast` | Model ID trên OpenRouter (gợi ý: `x-ai/grok-4-fast`, `x-ai/grok-4`, `x-ai/grok-2-1212`) |
| `--output-dir` | `research/x-viral-knowledge/[YYYY-MM-DD]/` | Thư mục output |
| `--format` | `json` | `json` \| `text` |
| `--no-save` | — | Không lưu file, chỉ stdout |

---

## Output

**Type:** research
**Location:** `research/x-viral-knowledge/[YYYY-MM-DD]/`

**Files produced:**
- `viral-knowledge-[topic-slug]-[period].json` — Raw data
- `viral-knowledge-[topic-slug]-[period].md` — Summary + chi tiết từng post

**JSON schema (mỗi item):**
```json
{
  "rank": 1,
  "author": "@handle",
  "post_type": "thread|single|quote",
  "title_or_hook": "Dòng đầu / headline của post",
  "summary": "Tóm tắt 3-5 câu nội dung kiến thức chính",
  "key_takeaways": ["tip 1", "tip 2", "tip 3"],
  "knowledge_value": 9,
  "virality_signal": "high|medium|low",
  "url": "https://x.com/...",
  "tags": ["claude", "prompt", "agent"]
}
```

Trường `knowledge_value` (1-10) ước lượng mức độ giá trị kiến thức, dùng để rank downstream.

---

## Workflow khi nhận yêu cầu

### Bước 1: Xác định topic
Nếu user không nói cụ thể → default `Claude.ai`. Nếu user nói "AI hot" → topic rộng như `AI agent` / `AI coding`.

### Bước 2: Chạy script
```bash
uv run .claude/skills/mkt-xcom-viral-knowledge-finder/scripts/search_x_viral_knowledge.py \
    --topic "<topic>" --period <period> --limit <n>
```

### Bước 3: Trình bày top list
Tóm tắt cho user:
- `rank. @author [knowledge_value/10] — title_or_hook`
- Key takeaways dạng bullet
- Link X.com (nếu có)

Ưu tiên post có `knowledge_value >= 7` và `post_type = thread`.

### Bước 4: Gợi ý content (tùy chọn)
Với mỗi post chất lượng → suggest:
- **Pillar 1**: Repurpose thread thành video tutorial Việt hóa
- **Pillar 3**: "Tuần này trên X có gì hay về Claude" — tổng hợp list
- **Facebook post**: `mkt-xpost-to-facebook-knowledge` để convert thẳng sang bài Facebook

---

## Filtering Rules (built-in)

Script prompt Grok chỉ trả về posts thỏa mãn:
- **Loại bỏ**: pure news ("OpenAI releases X"), memes, shitposts, hype without substance, ads, affiliate spam
- **Giữ lại**: threads giải thích concept, tips/tricks actionable, workflow breakdowns, comparison/review có phân tích, prompt templates, case studies với learnings cụ thể

---

## Quality Criteria

GOOD output:
- [x] `knowledge_value` đa số ≥ 7
- [x] `summary` có substance (không chỉ "post viral về X")
- [x] `key_takeaways` ≥ 2 items mỗi post
- [x] Mix được thread + single post chất lượng
- [x] URL hợp lệ (nếu Grok trả về)

BAD output:
- [ ] Toàn news headline không phải knowledge
- [ ] `summary` chung chung, không có tips/framework
- [ ] Bias về 1 author duy nhất (cần diversity)
- [ ] Trùng hoàn toàn với `mkt-ai-news-aggregator` output

---

## Integration với skills khác

| Downstream | Cách dùng |
|------------|-----------|
| `mkt-xpost-to-facebook-knowledge` | Convert 1 post → bài Facebook tiếng Việt |
| `mkt-content-repurposer` | 1 thread dài → multi-format content |
| `mkt-news-to-content-brief` | Rank list theo audience relevance |
| `mkt-create-script-short-video-v2-vn` | Pick 1 tip → viết script ngắn |
| `mkt-content-knowledge-compiler` | Compile insights vào knowledge base |

---

## Troubleshooting

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `OPENROUTER_API_KEY not set` | Thiếu env | Thêm vào `.env` |
| `HTTP 401` | Key sai / hết credit | Check OpenRouter dashboard |
| `HTTP 404 model_not_found` | Model ID không hợp lệ | Thử `--model x-ai/grok-2-1212` |
| Items toàn news chứ không phải knowledge | Grok không phân biệt tốt | Thêm từ khóa cụ thể hơn ("thread", "tutorial", "how to") vào `--topic` |
| JSON parse fail | Grok trả plain text | Script tự fallback, re-run hoặc đổi model |
| Kết quả lặp lại giữa các lần chạy | Grok không có live X search qua OpenRouter — dựa vào training/web | Dùng `mkt-ai-news-aggregator/search_x_posts.py` (xAI API trực tiếp) cho real-time |

---

## Giới hạn quan trọng

**Grok qua OpenRouter KHÔNG có X real-time search tool** như khi gọi xAI API trực tiếp. Kết quả dựa trên:
- Training data của Grok
- Knowledge được cập nhật trong model
- Reasoning về topic

→ Nếu cần **real-time** trending posts → dùng `mkt-ai-news-aggregator/scripts/search_x_posts.py` (xAI direct).
→ Skill này phù hợp khi cần **curated knowledge** có chiều sâu, không cần ngay hôm nay.

---

## Scripts

- `scripts/search_x_viral_knowledge.py` — Main search script qua OpenRouter → Grok.
