---
name: mkt-broll-image
description: "Tạo ảnh b-roll minh họa cho video ngắn bằng AI (AI33/Grok-2 hoặc Nano Banana Pro). Dùng khi production plan cần visual concept, minh họa ý tưởng, hoặc ảnh AI thay cho screenshot. USE WHEN user says 'tạo ảnh broll', 'tạo ảnh cho video', 'generate broll image', 'tạo visual cho video', 'ảnh minh họa video', 'broll image', 'tạo ảnh concept', 'AI image for video', 'ảnh AI cho video ngắn', 'tạo ảnh từ prompt video'."
---

# B-Roll Image Generator for Short Videos

Tạo ảnh minh họa concept/b-roll cho video ngắn (TikTok, Reels, Shorts) bằng AI image generation.

## Khi nào dùng

- Production plan có segment type `visual` hoặc `custom` cần ảnh minh họa concept
- Không có screenshot thật (website không phù hợp, concept trừu tượng)
- Cần ảnh minh họa: AI workflow, tech concept, comparison, metaphor
- Grok-prompts.md liệt kê prompts cho visual segments

## Providers

| Provider | Model | Ưu điểm | Key |
|----------|-------|---------|-----|
| `ai33` | Grok-2 Image | Tốt cho concept art, minh họa, chất lượng cao | `AI33_KEY` |
| `nano` | Gemini Flash Image | Text rendering tốt hơn, nhanh | `GEMINI_API_KEY` |

## Workflow

### Bước 1: Xác định ảnh cần tạo

Từ input (production plan, grok-prompts.md, hoặc yêu cầu user), xác định:
- Danh sách ảnh cần tạo (tên file, mô tả nội dung)
- Aspect ratio: `9:16` (vertical video) hoặc `1:1` (square)
- Provider: `ai33` (default) hoặc `nano`
- Output directory

### Bước 2: Viết prompt cho từng ảnh

**Quy tắc prompt cho b-roll video:**

1. **Vertical-first** — Mô tả composition cho 9:16 (portrait)
2. **Bold & clear** — Ảnh sẽ hiển thị 3-6 giây, cần dễ nhận biết ngay
3. **No small text** — Không đưa text nhỏ vào ảnh (caption sẽ overlay sau)
4. **High contrast** — Dark/vibrant background để chữ caption trắng dễ đọc
5. **Concept over literal** — Minh họa ý tưởng, không cần chính xác 100%

**Template prompt:**

```
[Mô tả cảnh/concept chính]. 
[Chi tiết composition — foreground, background, lighting].
Style: [cinematic/tech/minimal/editorial]. 
Vertical 9:16 portrait orientation. High contrast. Bold visual.
No text, no watermarks, no UI elements.
```

**Ví dụ prompt theo loại content:**

| Loại | Prompt pattern |
|------|---------------|
| Tech concept | "A futuristic visualization of [concept]. Glowing neural networks, dark background with blue/purple accents. Cinematic lighting." |
| Before/After | "Split screen showing [old way] on left (muted, gray) vs [new way] on right (vibrant, glowing). Dark tech aesthetic." |
| Workflow | "Isometric 3D illustration of [workflow steps]. Connected nodes, flowing data, modern tech style. Dark background." |
| AI/Robot | "A sleek AI assistant [doing action]. Holographic interface, clean futuristic design. Blue and purple color scheme." |
| Warning/Alert | "Dramatic visual of [risk/problem]. Red warning accents, dark moody atmosphere. Cinematic composition." |

### Bước 3: Generate ảnh

```bash
# AI33 (Grok-2) — default
python3 .claude/skills/image-post-creator/scripts/generate.py "<prompt>" \
  -o /path/to/assets/segment-name.png \
  -ar 9:16 \
  -p ai33 \
  -v

# Nano Banana Pro (Gemini)
python3 .claude/skills/image-post-creator/scripts/generate.py "<prompt>" \
  -o /path/to/assets/segment-name.png \
  -ar 9:16 \
  -p nano \
  --size 2K \
  -v
```

**Batch generate nhiều ảnh:**

```bash
# Chạy từng ảnh, mỗi lệnh 1 file
for i in 1 2 3; do
  python3 .claude/skills/image-post-creator/scripts/generate.py "<prompt_$i>" \
    -o /path/to/assets/seg${i}.png -ar 9:16 -p ai33 -v
done
```

### Bước 4: Verify kết quả

```bash
# Kiểm tra file tồn tại và kích thước
for f in /path/to/assets/*.png; do
  echo "$(basename $f): $(du -h "$f" | cut -f1) | $(sips -g pixelWidth -g pixelHeight "$f" 2>/dev/null | awk '/pixel/{printf $2"x"}')"
done
```

- File phải > 50KB
- Ảnh 9:16 portrait orientation
- Không có text/watermark không mong muốn

### Bước 5: Tích hợp vào video production

Sau khi tạo xong, ảnh sẵn sàng cho:
- **Ken Burns effect** — convert sang video bằng ffmpeg (zoom/pan)
- **Remotion composition** — dùng trực tiếp làm visual segment
- **Custom overlay** — chèn vào production plan

```bash
# Convert ảnh sang video Ken Burns (zoom in 6s)
ffmpeg -loop 1 -i segment.png -vf "scale=1080:1920,zoompan=z='min(zoom+0.001,1.3)':d=180:s=1080x1920:fps=30" \
  -t 6 -c:v libx264 -pix_fmt yuv420p segment.mp4
```

## Aspect Ratios

| Video format | Aspect ratio | Dùng khi |
|-------------|-------------|----------|
| TikTok/Reels/Shorts | `9:16` | Vertical video (default) |
| YouTube | `16:9` | Horizontal video |
| Square | `1:1` | Instagram feed |

## Error Handling

| Lỗi | Xử lý |
|------|--------|
| `AI33_KEY not found` | Set `AI33_KEY` trong `.env` |
| `GEMINI_API_KEY not found` | Set `GEMINI_API_KEY` trong `.env` |
| Timeout AI33 | Retry hoặc switch sang `nano` |
| Ảnh quá tối/sáng | Thêm "well-lit, balanced exposure" vào prompt |
| Có text không mong muốn | Thêm "absolutely no text, no labels, no watermarks" |

## Tham chiếu

- Script generate: `.claude/skills/image-post-creator/scripts/generate.py`
- Screenshot b-roll: `.claude/skills/mkt-broll-screenshot/` (cho web screenshot)
- Production plan: `.claude/skills/plan-short-video-edit/` (upstream)
- Video editor: `.claude/skills/heygen-remotion-short-video-editor/` (downstream)
