---
name: github-trend-finder
description: Tìm top GitHub trending repositories (daily/weekly/monthly) để làm content AI/tech. Scrape github.com/trending, lọc theo language, lưu JSON + Markdown. USE WHEN user says 'github trend hôm nay', 'top github trending', 'tìm github trending', 'github trending daily', 'top 10 github repo', 'research github trend', 'github trend for content', 'lấy github trending', 'github hot hôm nay', 'trending repo'.
---

# GitHub Trend Finder

Lấy top repo trending trên `github.com/trending` (daily mặc định) kèm description, language, stars today, total stars, forks. Output JSON + Markdown để seed cho content AI/tech (Pillar 1 & Pillar 3).

---

## When to Use

- User muốn top 10 repo trending trong ngày để làm content
- Cần seed tech news / AI tool hot cho video ngắn, Facebook post
- Bổ trợ cho `mkt-ai-news-aggregator` (GitHub source) và `mkt-news-to-content-brief`

---

## Prerequisites

```bash
pip3 install requests beautifulsoup4
```

Không cần API key — scrape trực tiếp HTML.

---

## Usage

```bash
# Top 10 trending hôm nay (all languages)
python3 .claude/skills/github-trend-finder/scripts/fetch_github_trends.py

# Filter language
python3 .claude/skills/github-trend-finder/scripts/fetch_github_trends.py --language python

# Weekly TypeScript, lưu custom dir
python3 .claude/skills/github-trend-finder/scripts/fetch_github_trends.py \
    --language typescript --since weekly --limit 10 \
    --output-dir research/github-trend/weekly

# In ra stdout (JSON) không lưu file
python3 .claude/skills/github-trend-finder/scripts/fetch_github_trends.py --format stdout
```

### Options

| Flag | Default | Mô tả |
|------|---------|-------|
| `--language` | `all` | `python`, `typescript`, `javascript`, `go`, `rust`, `all`... |
| `--since` | `daily` | `daily` \| `weekly` \| `monthly` |
| `--limit` | `10` | Số repo tối đa |
| `--output-dir` | `research/github-trend/[YYYY-MM-DD]/` | Thư mục output |
| `--format` | `both` | `json` \| `md` \| `both` \| `stdout` |

---

## Output

**Type:** research
**Location:** `research/github-trend/[YYYY-MM-DD]/`

**Files produced:**
- `trending-[lang]-[since].json` — Raw data cho downstream skills
- `trending-[lang]-[since].md` — Bảng summary + chi tiết từng repo

**JSON schema (mỗi repo):**
```json
{
  "rank": 1,
  "owner": "openai",
  "name": "codex",
  "full_name": "openai/codex",
  "url": "https://github.com/openai/codex",
  "description": "Lightweight coding agent that runs in your terminal",
  "language": "Rust",
  "stars_today": 1234,
  "total_stars": 45678,
  "forks": 2345
}
```

---

## Workflow khi nhận yêu cầu

### Bước 1: Chạy script
Mặc định daily/all. Nếu user chỉ định ngôn ngữ hoặc khoảng thời gian → thêm `--language` / `--since`.

### Bước 2: Đọc kết quả
Script in ra JSON `{status, count, source_url, written: [paths]}`. Read file Markdown để nắm nhanh top list.

### Bước 3: Trình bày cho user
Tóm tắt top 10 dạng bullet: `rank. owner/name — stars_today ⭐ today — description`. Ưu tiên nhấn mạnh repo AI/tech phù hợp brand (AI agent, automation, dev tools, LLM).

### Bước 4: (Tùy chọn) Gợi ý content
Với mỗi repo phù hợp Pillar 1/3, đề xuất angle content ngắn:
- **Pillar 1 (AI Demo/Tutorial)**: Repo AI tool mới → video demo/review
- **Pillar 3 (AI News)**: Repo bất ngờ lên trending → news post "GitHub hôm nay có gì hot"

---

## Quality Criteria

GOOD output:
- [x] Có đủ 10 repo (hoặc = `--limit`)
- [x] `stars_today`, `total_stars`, `forks` đều parse được (không toàn 0)
- [x] `description` không rỗng với repo lớn
- [x] Markdown có cả bảng tổng quan + chi tiết từng repo
- [x] JSON parse được bằng downstream skill

BAD output:
- [ ] Parse fail do GitHub đổi HTML → cần debug selector
- [ ] Bị rate limit / chặn User-Agent → đổi header
- [ ] Trả về toàn repo non-tech (không filter được) → advise user thêm `--language`

---

## Integration với skills khác

| Downstream | Cách dùng |
|------------|-----------|
| `mkt-ai-news-aggregator` | Làm nguồn GitHub thay vì gọi lại scrape |
| `mkt-news-to-content-brief` | Feed JSON → rank theo audience relevance |
| `mkt-create-script-short-video` / `-v2-vn` | Pick top 1-3 repo → viết script |
| `mkt-build-in-public-post-creator` | "Tuần này trending có gì" post |

---

## Troubleshooting

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `No repos parsed` | GitHub đổi HTML hoặc chặn request | Update selector trong `parse_trending()`, xoay User-Agent |
| `ImportError: bs4` | Chưa cài BeautifulSoup | `pip3 install beautifulsoup4` |
| `HTTP 429` | Rate limit | Đợi vài phút, giảm tần suất chạy |
| Repo thiếu description | Repo trending mới, chưa có mô tả | OK — trường `description` rỗng |

---

## Scripts

- `scripts/fetch_github_trends.py` — Main scraper. Chạy:
  ```bash
  python3 .claude/skills/github-trend-finder/scripts/fetch_github_trends.py [OPTIONS]
  ```
