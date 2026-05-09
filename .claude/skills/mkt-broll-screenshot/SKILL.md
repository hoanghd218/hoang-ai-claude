---
name: mkt-broll-screenshot
description: "Chụp screenshot và quay video scroll b-roll từ trang web ở dạng điện thoại iPhone (mobile responsive) để làm visual chèn vào video ngắn. USE WHEN user says 'chụp ảnh repo', 'screenshot github', 'chụp web', 'b-roll screenshot', 'quay scroll', 'chụp ảnh trang web', 'capture mobile screenshot', 'lấy ảnh cho video', 'chụp ảnh điện thoại', 'screenshot mobile', 'quay video scroll web'. Also use when a production plan or grok-prompts.md references custom assets that need screenshots from URLs."
---

# B-Roll Screenshot & Scroll Video Capture

Chụp screenshot mobile-responsive và quay video scroll b-roll từ bất kỳ trang web nào, phục vụ làm visual cho video ngắn (TikTok, Reels, Shorts).

## Nguyên tắc cốt lõi

- **Luôn chụp ở dạng điện thoại** — iPhone 15 Pro (393x852 CSS, 3x retina, output 1179x1977px)
- **Dùng Chromium** — không dùng WebKit (cần cài riêng, hay lỗi)
- **Mobile responsive** — GitHub, Product Hunt, docs... đều render giao diện mobile thật
- **Hai chế độ**: screenshot tĩnh (PNG) hoặc quay scroll video (WebM)

## Workflow

### Bước 1: Xác định URLs và output

Từ input của user, xác định:
- Danh sách URLs cần chụp
- Tên file output cho mỗi URL (ví dụ: `auto-research-github`)
- Chế độ: `screenshot` (mặc định) hoặc `video` (scroll b-roll)
- Thư mục output (mặc định: `assets/` trong folder video hiện tại)

Input có thể là:
- User liệt kê trực tiếp URLs
- File `grok-prompts.md` hoặc `production-plan.json` chứa danh sách assets cần chụp
- Tên repo GitHub (tự search URL)

### Bước 2: Chạy script capture

Dùng script `scripts/capture.py` trong thư mục skill này.

**Chụp screenshot:**
```bash
python3 .claude/skills/mkt-broll-screenshot/scripts/capture.py screenshot \
  --urls "https://github.com/user/repo" \
  --names "repo-name" \
  --output-dir /path/to/assets/
```

**Quay scroll video:**
```bash
python3 .claude/skills/mkt-broll-screenshot/scripts/capture.py video \
  --urls "https://github.com/user/repo" \
  --names "repo-name" \
  --output-dir /path/to/assets/ \
  --scroll-px 1500 \
  --duration 8
```

**Nhiều URLs cùng lúc:**
```bash
python3 .claude/skills/mkt-broll-screenshot/scripts/capture.py screenshot \
  --urls "https://github.com/a/b,https://github.com/c/d" \
  --names "repo-a,repo-b" \
  --output-dir /path/to/assets/
```

### Bước 3: Kiểm tra kết quả

Sau khi chụp xong, verify:
- File tồn tại và có dung lượng hợp lý (>50KB cho screenshot, >200KB cho video)
- Dimensions đúng (1179x1977 cho screenshot)
- Liệt kê kết quả cho user xem

```bash
# Verify
for f in /path/to/assets/*.png; do
  sips -g pixelWidth -g pixelHeight "$f" 2>/dev/null | awk '/pixel/{printf $2" "}'
  ls -lh "$f" | awk '{print " | " $5 " | " $NF}'
done
```

## Tham số script

| Param | Mặc định | Mô tả |
|-------|----------|-------|
| `mode` | `screenshot` | `screenshot` hoặc `video` |
| `--urls` | (bắt buộc) | URLs cách nhau bởi dấu phẩy |
| `--names` | (bắt buộc) | Tên file output, cách nhau bởi dấu phẩy |
| `--output-dir` | `.` | Thư mục lưu file |
| `--scroll-px` | `1500` | Pixel scroll xuống (chỉ video mode) |
| `--duration` | `8` | Thời gian scroll giây (chỉ video mode, tối đa 10) |
| `--wait` | `1.5` | Giây chờ sau khi page load xong |

## Output

- Screenshot: `{name}.png` — 1179x1977px, mobile responsive
- Video: `{name}-broll.webm` — 1080x1920px, smooth scroll từ trên xuống

## Lưu ý kỹ thuật

- Script dùng Python Playwright với Chromium (đã cài sẵn)
- iPhone 15 Pro emulation: viewport 393x852, scale 3x, mobile user agent, touch enabled
- Page load: `wait_until="networkidle"`, timeout 15s, rồi chờ thêm 1.5s
- Video scroll: chia thành nhiều bước nhỏ (~100ms/bước) để tạo hiệu ứng mượt
- Chạy song song nếu nhiều URLs (mỗi URL một browser context riêng)
