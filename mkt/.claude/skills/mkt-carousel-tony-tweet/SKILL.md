---
name: mkt-carousel-tony-tweet
description: "Tạo ảnh carousel dạng tweet card với brand 'Tony Hoang Learn AI Automation' bằng Nano Banana Pro (qua ai33.pro). Nhận vào script nội dung, insight, hoặc ảnh mẫu carousel rồi render thành ảnh có avatar + name header giống tweet của Tony Hoang. Hỗ trợ cả tiếng Việt lẫn tiếng Anh. USE WHEN user says 'tạo carousel tony', 'carousel tweet', 'tạo ảnh tony hoang', 'carousel từ script', 'tweet card carousel', 'làm carousel kiểu drew huibregtse', 'tạo ảnh tweet style', 'nano banana carousel', 'carousel ai33', 'tạo slides tweet tony'."
---

# Tony Hoang Tweet-Style Carousel

Render ảnh carousel theo layout tweet card (giống Drew Huibregtse, Dan Koe, Justin Welsh...) với brand của Tony Hoang. Input là script/nội dung hoặc ảnh carousel mẫu để bắt chước cấu trúc — output là các slide PNG sẵn sàng đăng IG/LinkedIn/X.

## Brand constants

**Những giá trị này KHÔNG được thay đổi giữa các lần chạy** — đó là brand identity:

| Field | Value |
|-------|-------|
| Profile name | `Tony Hoang Learn AI Automation` |
| Handle | `@tranvanhoang.com` |
| Verified badge | Blue checkmark (Twitter/X-style) bên cạnh name |
| Avatar path | `workspace/assets/brand/tony-avatar.jpg` |
| Default aspect ratio | `4:5` (1080x1350 — IG carousel chuẩn) |
| Background | Pure white `#FFFFFF` |
| Text color | Near-black `#111111` |
| Prompt box bg | Light gray `#F5F5F5` với rounded corners |
| Checkmark color | Green `#22C55E` bold ✓ |
| Font feel | Clean sans-serif, Twitter-like (Inter/Helvetica/system-ui) |

**Kiểm tra avatar trước khi chạy:**

```bash
ls -lh workspace/assets/brand/tony-avatar.jpg
```

Nếu chưa có, hỏi user cung cấp — KHÔNG generate mà thiếu avatar (ảnh sẽ mất brand consistency).

## Input modes

Skill nhận 1 trong 3 loại input:

1. **Script/nội dung thô** — User paste content (VN/EN) muốn làm carousel. Skill tự chia slide.
2. **Insight/bullet list** — User đưa key points, skill biến mỗi point thành 1 slide.
3. **Ảnh carousel mẫu** — User gửi ảnh tham khảo (như của Drew Huibregtse). Skill phân tích layout, áp brand Tony.

Hỏi user nếu không rõ mode.

## Workflow

### Bước 1 — Xác định ngôn ngữ & số slide

Hỏi user nếu không rõ:
- **Ngôn ngữ**: Tiếng Việt hay English? (mặc định = ngôn ngữ của script input)
- **Số slide**: Thường 6-10 slide. Slide 1 luôn là hook, slide cuối luôn là CTA/summary.

### Bước 2 — Phân loại layout từng slide

Áp dụng 2 layout types:

#### Layout A — Tweet Card Classic
Cho slide kể chuyện, reasoning, quote, insight dài. Chỉ header + text body.

```
[AVATAR] Tony Hoang Learn AI Automation ✓
         @tranvanhoang.com

[Body text — prose, 3-6 short paragraphs]
[Có thể bold các từ khóa quan trọng]
```

#### Layout B — Prompt Showcase
Cho slide dạng "Prompt N (Title)" + prompt box + how-to + result. Dùng cho carousel kiểu actionable tips/prompts.

```
[AVATAR] Tony Hoang Learn AI Automation ✓
         @tranvanhoang.com

**Prompt N (Title)**

[Gray rounded box]
  Nội dung prompt ở đây...
[/box]

How to use it:
Hướng dẫn 2-3 câu cách dùng.

Result you get:
✓ Point 1
✓ Point 2
✓ Point 3
```

**Quyết định layout:** Nếu nội dung có "prompt" / "công thức" / "framework template" → Layout B. Còn lại → Layout A.

### Bước 3 — Soạn carousel plan

Lưu plan tại `workspace/content/<date>/carousel/<slug>/plan.json`:

```json
{
  "topic": "...",
  "language": "vi",
  "aspect_ratio": "4:5",
  "slides": [
    {
      "index": 1,
      "layout": "A",
      "prompt": "<full Nano Banana prompt — xem references/prompt-templates.md>",
      "output": "workspace/content/<date>/carousel/<slug>/slide_01.png"
    }
  ]
}
```

Trước khi generate, **show plan cho user review** — đặc biệt phần text body của mỗi slide. User có thể edit wording trước khi tốn credits.

### Bước 4 — Build prompts

Với mỗi slide, build prompt theo template trong `references/prompt-templates.md`. Điểm quan trọng:

- **Mô tả avatar** trong prompt là redundant vì mình pass reference image, NHƯNG vẫn mô tả ngắn (VD: "Vietnamese man with short dark hair, wearing cap") để Nano Banana biết chỗ đặt. Reference image sẽ lock face consistency.
- **Text trong ảnh phải viết nguyên văn** (Nano Banana Pro render chính xác). KHÔNG paraphrase trong prompt — paste chính xác chữ muốn hiện.
- Dấu tiếng Việt viết đầy đủ trong prompt (có dấu). Nano Banana Pro render được.
- Không đưa pixel size (`"28px"`, `"16pt"`) vào prompt — model sẽ render literal chữ đó vào ảnh.

### Bước 5 — Generate

```bash
python3 .claude/skills/mkt-carousel-tony-tweet/scripts/generate_carousel.py \
  --plan workspace/content/<date>/carousel/<slug>/plan.json \
  --out-dir workspace/content/<date>/carousel/<slug>/ \
  --avatar workspace/assets/brand/tony-avatar.jpg \
  -ar 4:5 \
  -v
```

Flags:
- `--avatar` — pass avatar làm reference image (image_urls + input_images fields). Giúp face consistent giữa các slide.
- `--plan` — batch render từ JSON plan.
- `-ar` — override aspect ratio nếu cần (9:16 cho Stories, 1:1 cho X/Twitter).

Single slide ad-hoc:

```bash
python3 .claude/skills/mkt-carousel-tony-tweet/scripts/generate_carousel.py \
  --prompt "$(cat slide_prompt.txt)" \
  -o slide_test.png \
  --avatar workspace/assets/brand/tony-avatar.jpg \
  -ar 4:5 -v
```

### Bước 6 — Verify & iterate

Kiểm tra output:

```bash
for f in workspace/content/<date>/carousel/<slug>/slide_*.png; do
  sips -g pixelWidth -g pixelHeight "$f" 2>/dev/null | grep pixel
done
```

**Common issues & fixes:**

| Issue | Fix |
|-------|-----|
| Text bị sai chính tả (dấu TV) | Bỏ dấu khó (VD: "ư" → "u") nếu xuất hiện nhiều, hoặc retry 1-2 lần |
| Avatar không giống | Kiểm tra path avatar đúng, avatar file < 2MB. Retry. |
| Layout lệch | Prompt thêm "header section at top, text body below with generous padding" |
| Verified checkmark sai màu | Prompt thêm "Twitter-blue verified checkmark icon, filled" |
| Name không đủ dài | Prompt thêm "profile name in bold, fits on one line" |

Nếu 1 slide vẫn không đạt sau 2 retry, dùng `--plan` với plan chỉ chứa slide đó để re-generate riêng.

## Reference files

- `references/prompt-templates.md` — Full prompt templates cho Layout A/B kèm ví dụ VN/EN
- `references/sample-analysis.md` — Phân tích design các ảnh mẫu Drew Huibregtse để tham chiếu

## Output structure

```
workspace/content/<date>/carousel/<slug>/
├── source.md         # Script/insight gốc user cung cấp
├── plan.json         # Carousel plan với prompts
├── slide_01.png
├── slide_02.png
├── ...
└── README.md         # Caption + hashtag gợi ý cho post
```

## When NOT to use this skill

- User muốn carousel cho LinkedIn dark tech style → dùng `mkt-linkedin-carousel-image`
- User muốn educational slide (chalkboard dev explainer) → dùng `mkt-edu-slide-nano`
- User muốn Facebook post image (typography-based) → dùng `image-post-creator`
- User muốn 2 carousel variant IG/TikTok từ transcript → dùng `mkt-carousel-creator` để lên content + skill này để render

Skill này riêng cho **tweet-card branded carousel của Tony Hoang** với avatar consistency.
