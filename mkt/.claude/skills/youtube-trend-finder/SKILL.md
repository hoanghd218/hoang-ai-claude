---
name: youtube-trend-finder
description: Fetch latest videos from subscribed YouTube channels using YouTube Data API v3. USE WHEN user says 'tìm video trend', 'tìm video trending', 'video hot hôm nay', 'video mới hôm nay', 'video mới từ kênh', 'check video mới', 'search youtube trend', 'find trending videos', 'video nào đang hot', 'channel monitor'.
---

# YouTube Channel Video Finder

Lấy danh sách **video dài** (long-form, > 5 phút) mới nhất từ các kênh YouTube đã đăng ký theo dõi. **Tự động lọc bỏ video ngắn** (video < 5 phút). Trả về tên video, link, thumbnail, ngày đăng và số views — gọi trực tiếp YouTube Data API v3.

---

## When to Use

- User muốn xem video mới nhất từ các kênh theo dõi
- User muốn check video hôm nay / tuần này từ danh sách kênh
- User muốn lấy danh sách video kèm thumbnail và số view để nghiên cứu nội dung

---

## Default Channels

| Handle | Channel |
|--------|---------|
| `@BenAI92` | Ben AI |
| `@chiefleverageofficer` | Chief Leverage Officer |
| `@ColeMedin` | Cole Medin |
| `@DavidOndrej` | David Ondrej |
| `@AlexFinnOfficial` | Alex Finn |

---

## Prerequisites

1. **API Key đã được set** trong `.env`:
   ```
   YOUTUBE_API_KEY=your_actual_api_key_here
   ```

2. **Dependencies đã cài**:
   ```bash
   pip3 install requests python-dotenv
   ```

3. **YouTube Data API v3 đã enable** tại [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com)

---

## Usage

### Cú pháp

```bash
python3 .claude/skills/youtube-trend-finder/scripts/search_trends.py [OPTIONS]
```

### Date Filters

| Filter  | Ý nghĩa              | Khoảng thời gian |
|---------|----------------------|------------------|
| `today` | Video hôm nay (mặc định) | 24 giờ qua  |
| `week`  | Video trong tuần     | 7 ngày qua       |
| `month` | Video trong tháng    | 30 ngày qua      |

### Ví dụ lệnh

```bash
# Video mới hôm nay từ tất cả kênh mặc định
python3 .claude/skills/youtube-trend-finder/scripts/search_trends.py

# Video trong tuần
python3 .claude/skills/youtube-trend-finder/scripts/search_trends.py --date week

# Chỉ định kênh khác
python3 .claude/skills/youtube-trend-finder/scripts/search_trends.py --channels "@BenAI92,@ColeMedin"

# Xuất JSON
python3 .claude/skills/youtube-trend-finder/scripts/search_trends.py --format json

# Lưu file
python3 .claude/skills/youtube-trend-finder/scripts/search_trends.py --date week --format json --output research/youtube/trends/weekly.json
```

### Options

```
--channels        Danh sách @handle (phẩy ngăn cách). Mặc định: 5 kênh đã cấu hình
--date, -d        today | week | month (mặc định: today)
--format, -f      markdown | json (mặc định: markdown)
--output, -o      Lưu kết quả ra file
```

---

## Output Format

**Lưu ý:** Script tự động lọc bỏ YouTube Shorts (video dưới 60 giây). Chỉ trả về video dài (long-form).

Mỗi video trả về:

| Field           | Mô tả                                    |
|-----------------|------------------------------------------|
| `title`         | Tên video                                |
| `url`           | Link YouTube                             |
| `channel`       | Tên kênh                                 |
| `thumbnail_url` | URL ảnh thumbnail (chất lượng cao nhất)  |
| `published_at`  | Ngày đăng (ISO 8601)                     |
| `view_count`    | Số lượt xem                              |

---

## API Quota

Script sử dụng playlist API thay vì search API để tiết kiệm quota:

| API Call | Cost | Per Run (5 channels) |
|----------|------|---------------------|
| `channels.list` (resolve handle) | 1 unit | 5 units |
| `playlistItems.list` (get videos) | 1 unit | 5 units |
| `videos.list` (get views + duration) | 1 unit | 1-2 units |
| **Total** | | **~12 units** |

So với search API (500 units/run), tiết kiệm ~98% quota.

**Shorts filtering:** Script fetch thêm `contentDetails` để lấy duration, tự động lọc bỏ video < 60 giây (YouTube Shorts).

---

## Workflow khi nhận yêu cầu

### Bước 1: Chạy script

```bash
python3 .claude/skills/youtube-trend-finder/scripts/search_trends.py --date [FILTER]
```

### Bước 2: Hiển thị kết quả

Trình bày danh sách video mới, bao gồm:
- Tên video + link
- Kênh
- Số views
- Ngày đăng
- Thumbnail

### Bước 3: (Tùy chọn) Lưu kết quả

```bash
python3 .claude/skills/youtube-trend-finder/scripts/search_trends.py --date [FILTER] --output research/youtube/trends/[date].json
```

---

## Troubleshooting

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `YOUTUBE_API_KEY not found` | Key chưa set | Thêm vào `.env` |
| `Could not resolve @handle` | Handle sai hoặc API lỗi | Kiểm tra handle chính xác |
| `403` | API key sai hoặc quota hết | Kiểm tra Google Cloud Console |
| `No videos found` | Kênh chưa đăng video trong khoảng thời gian | Thử `--date week` |

---

## Output Location

**Type:** research
**Location:** `research/youtube/trends/`
