---
name: notion-video-trend-sync
description: Push YouTube video data (title, URL, views, thumbnail, transcript) to the Notion "AI YouTube Videos" database. USE WHEN user says 'đẩy video lên notion', 'sync video notion', 'lưu video vào notion', 'push to notion', 'save video to notion', 'notion video sync'.
---

# Notion Video Trend Sync

Push YouTube video data to the **🎬 YouTube Videos** Notion database using the Notion MCP server.

---

## When to Use

- After finding trending videos with `youtube-trend-finder`
- After extracting transcripts with `youtube-transcript`
- After extracting insights with `insight-extractor`
- When user wants to save video research results to Notion
- When batch-importing video data to the tracking database

---

## Prerequisites

1. **Notion MCP server** configured and connected
2. **Environment variables** in `.env`:
   ```
   NOTION_DATABASE_VIDEO_TREND_ID=31bab9e5e7408006998edd545ae23695
   NOTION_DATASOURCE_VIDEO_TREND_ID=31bab9e5-e740-80c1-9176-000b44bf2aed
   ```

---

## Database Schema

**Database:** 🎬 YouTube Videos
**URL:** `https://www.notion.so/31bab9e5e7408006998edd545ae23695`
**Data Source ID:** `31bab9e5-e740-80c1-9176-000b44bf2aed`

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `Name` | title | Yes | Video title |
| `Link` | url | No | YouTube video URL |
| `Views` | number | No | View count |
| `Thumbnail` | file | No | Thumbnail URL (external file) |
| `Summary` | text | No | Video summary (under 200 words) |
| `Transcript Link` | url | No | Link to transcript file or page |
| `Insight` | text | No | Key insights extracted from video |
| `Status` | select | No | Workflow status |
| `Date` | date | No | Video publish date |

### Status Options (select)

Available values: `Ngân hàng`, `Sử dụng làm content`

---

## Usage

### Step 1: Prepare Video Data

Collect video data from `youtube-trend-finder` and `insight-extractor` output:

```json
{
  "title": "Video Title",
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "views": 125000,
  "thumbnail_url": "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg",
  "published_at": "2026-03-06",
  "summary": "Under 200 words summary...",
  "insights": [
    {"type": "Framework", "title": "...", "explanation": "..."},
    {"type": "Warning", "title": "...", "explanation": "..."}
  ]
}
```

### Step 2: Format Insights for Notion

Convert insights array to a formatted string:

```
• Framework: The 3-step content system — First extract ideas, then batch produce, finally distribute.
• Warning: Don't automate before you validate — Automating a broken process produces bad content faster.
```

### Step 3: Push to Notion via MCP

Use the Notion MCP `notion-create-pages` tool with data_source_id:

```json
{
  "parent": {
    "data_source_id": "31bab9e5-e740-80c1-9176-000b44bf2aed"
  },
  "pages": [
    {
      "properties": {
        "Name": "Video Title Here",
        "Link": "https://www.youtube.com/watch?v=VIDEO_ID",
        "Views": 125000,
        "Summary": "Under 200 words summary of the video...",
        "Insight": "• Framework: Title — Explanation\n• Warning: Title — Explanation",
        "Status": "Ngân hàng",
        "date:Date:start": "2026-03-06",
        "date:Date:is_datetime": 0
      },
      "content": "## Transcript\n\nFull transcript content here..."
    }
  ]
}
```

### Step 4: Batch Import (Multiple Videos)

For multiple videos, batch them into a single `notion-create-pages` call (max 100 pages per call):

```json
{
  "parent": {
    "data_source_id": "31bab9e5-e740-80c1-9176-000b44bf2aed"
  },
  "pages": [
    {
      "properties": {
        "Name": "Video 1 Title",
        "Link": "https://www.youtube.com/watch?v=ID1",
        "Views": 50000,
        "Summary": "Summary of video 1",
        "Insight": "• Framework: ...\n• Paradigm Shift: ...",
        "Status": "Ngân hàng",
        "date:Date:start": "2026-03-06",
        "date:Date:is_datetime": 0
      }
    },
    {
      "properties": {
        "Name": "Video 2 Title",
        "Link": "https://www.youtube.com/watch?v=ID2",
        "Views": 80000,
        "Summary": "Summary of video 2",
        "Insight": "• Warning: ...\n• Principle: ...",
        "Status": "Ngân hàng",
        "date:Date:start": "2026-03-06",
        "date:Date:is_datetime": 0
      }
    }
  ]
}
```

---

## Workflow

```
youtube-trend-finder (JSON output)
        │
        ▼
youtube-transcript (transcript text)
        │
        ▼
insight-extractor (summary + insights)
        │
        ▼
notion-video-trend-sync (push to Notion)
        │
        ▼
  Notion Database: 🎬 YouTube Videos
```

---

## Property Mapping

| Source Field | Notion Property | Transform |
|--------------|-----------------|-----------|
| `title` | `Name` | Direct |
| `url` | `Link` | Direct |
| `views` | `Views` | Direct (number) |
| `thumbnail_url` | `Thumbnail` | External file URL |
| `summary` | `Summary` | Under 200 words |
| `insights[]` | `Insight` | Format as bullet list |
| `published_at` | `Date` | ISO date format |
| — | `Status` | Default to `Ngân hàng` |
| transcript text | Page content | Markdown body |

### Insight Formatting

Convert JSON insights to text format:

```
Input:
[
  {"type": "Framework", "title": "3-step system", "explanation": "Extract, produce, distribute."},
  {"type": "Warning", "title": "Don't automate early", "explanation": "Fix process first."}
]

Output:
• Framework: 3-step system — Extract, produce, distribute.
• Warning: Don't automate early — Fix process first.
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `notion-create-pages failed` | MCP not connected | Verify Notion MCP server is running |
| `data_source_id not found` | Wrong ID | Use `31bab9e5-e740-80c1-9176-000b44bf2aed` |
| `Property not found` | Schema mismatch | Fetch database schema with `notion-fetch` to verify |
| `Rate limit` | Too many API calls | Batch pages (max 100) instead of individual calls |

---

## Quality Criteria

- Each video page has Name + Link + Views at minimum
- Summary is under 200 words, specific not generic
- Insights formatted as bullet list with type + title + explanation
- Status defaults to `Ngân hàng` for new entries
- Date is set to video publish date (not import date)
- Transcript (if available) is stored as page content
