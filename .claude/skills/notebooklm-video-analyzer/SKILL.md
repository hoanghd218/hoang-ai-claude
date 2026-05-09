---
name: notebooklm-video-analyzer
description: Analyze YouTube videos in Notion database using NotebookLM. Finds pages without NotebookLM links, adds YouTube URLs as NotebookLM sources, extracts AI insights/summary, and saves results back to Notion. USE WHEN user says 'analyze videos with notebooklm', 'process notion videos', 'notebooklm analyze', 'add notebooklm to videos', 'analyze youtube database', 'notebooklm insights for videos'.
---

# NotebookLM Video Analyzer

Processes YouTube videos from a Notion database through NotebookLM for AI-powered analysis. Finds pages missing NotebookLM links, creates analysis via NotebookLM, and saves insights back to Notion.

---

## When to Use

- User wants to analyze YouTube videos stored in a Notion database using NotebookLM
- User wants to batch-process videos that don't have NotebookLM analysis yet
- User wants AI-generated summaries and insights for YouTube content

---

## Prerequisites

- **NotebookLM MCP** configured and authenticated (`nlm login --check`)
- **Notion MCP** configured with access to the target database
- A **processing notebook** in NotebookLM (reused for all analyses)

---

## Configuration

```yaml
# Notion Database
database_id: "6fa63945-025a-4ab8-bf27-6a754bd0ed22"
data_source_id: "885a44e0-6843-479c-9b2d-eafdb31720ae"

# Processing Notebook (reused — notebook_create API is currently broken)
processing_notebook_id: "d74a5dac-b88b-4b09-b488-bbf2c1d5d649"

# Notion Database Schema (key columns)
columns:
  title: "Title"           # title type
  video_link: "Video Link" # url type — YouTube URL
  notebooklm_link: "NotebookLM Link" # url type — link to NotebookLM notebook
  summary: "Summary"       # text type — AI-generated summary
  note: "Note"             # text type — additional notes
  topic: "Topic"           # multi_select type
```

---

## Workflow

### Phase 1: DISCOVER — Find Unprocessed Pages

1. Use `notion-search` on the data source to find video pages
2. Use `notion-fetch` on each page to check if `NotebookLM Link` is empty
3. Collect pages that have a `Video Link` but no `NotebookLM Link`

### Phase 2: ANALYZE — Process via NotebookLM

For each unprocessed page:

1. **Add YouTube source** to the processing notebook:
   ```
   nlm source add <processing_notebook_id> --url <youtube_url> --wait
   ```
   This returns a `source_id` when processing completes.

2. **Get source-level summary** (focused on this single video):
   ```
   nlm source describe <source_id>
   ```
   Returns: summary text + keyword chips

3. **Query for deeper insights** (optional, for richer analysis):
   ```
   nlm notebook query <processing_notebook_id> \
     "Provide key insights, actionable tips, and main takeaways from this video. \
      Structure as: Summary (2-3 sentences), Key Insights (bullet points), \
      Actionable Tips (bullet points), Keywords (comma-separated)."
   ```

4. **Get NotebookLM link**:
   ```
   Link format: https://notebooklm.google.com/notebook/<processing_notebook_id>
   ```

### Phase 3: SAVE — Write Results to Notion

**Primary method** — Add comment to the page (since `update-page` is currently broken):

Use `notion-create-comment` on the page with:
- NotebookLM Link
- AI Summary
- Keywords
- Key Insights

**Format:**
```json
{
  "page_id": "<page_id>",
  "rich_text": [
    {"type": "text", "text": {"content": "NotebookLM Analysis\n\n"}, "annotations": {"bold": true}},
    {"type": "text", "text": {"content": "Link: ", "link": null}, "annotations": {"bold": true}},
    {"type": "text", "text": {"content": "<notebooklm_url>", "link": {"url": "<notebooklm_url>"}}},
    {"type": "text", "text": {"content": "\n\nSummary: <summary>\n\nKeywords: <keywords>\n\nKey Insights:\n<insights>"}}
  ]
}
```

**When update-page is fixed**, switch to:
```json
{
  "page_id": "<page_id>",
  "command": "update_properties",
  "properties": {
    "NotebookLM Link": "<notebooklm_url>",
    "Summary": "<summary_text>"
  }
}
```

### Phase 4: CLEANUP — Remove Source

After saving results, clean up the processing notebook:
```
nlm source delete <source_id> --confirm
```

This keeps the processing notebook clean for the next video.

---

## Known Limitations

| Issue | Status | Workaround |
|-------|--------|------------|
| `notebook create` API broken | Google RPC change | Reuse a single processing notebook |
| `notion update-page` broken | Notion MCP bug | Use `notion-create-comment` instead |
| Notebook has 500 limit | Google limit | Clean up sources after processing |

---

## Example Run (Single Page)

```bash
# Step 1: Find page without NotebookLM link
# Use notion-search + notion-fetch to identify target pages

# Step 2: Add YouTube source
nlm source add d74a5dac-b88b-4b09-b488-bbf2c1d5d649 \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" --wait

# Step 3: Get AI analysis
nlm source describe <source_id>
nlm notebook query d74a5dac-b88b-4b09-b488-bbf2c1d5d649 \
  "Key insights and actionable tips from this video"

# Step 4: Save to Notion via comment
# Use notion-create-comment with formatted results

# Step 5: Cleanup
nlm source delete <source_id> --confirm
```

---

## Batch Processing

When processing multiple pages:
1. Process **one video at a time** (add source → analyze → save → delete source)
2. Wait for source processing to complete before querying
3. Present results to user for review after each video
4. Ask for confirmation before proceeding to next video (unless `--auto` flag)

---

## Query Templates

### Standard Summary Query
```
Provide a comprehensive summary of this video in 3-4 sentences. Include the main topic,
key arguments, and practical takeaways.
```

### Insight Extraction Query
```
Extract the top 5 key insights from this video. For each insight, provide:
1. The insight (one sentence)
2. Why it matters (one sentence)
3. How to apply it (one sentence)
```

### Vietnamese Summary Query (for brand voice)
```
Tóm tắt video này bằng tiếng Việt, 3-4 câu. Nêu chủ đề chính,
các luận điểm quan trọng, và bài học thực tế có thể áp dụng ngay.
```
