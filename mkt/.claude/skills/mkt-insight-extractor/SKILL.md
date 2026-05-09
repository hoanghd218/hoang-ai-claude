---
name: mkt-insight-extractor
description: Extract key insights from video transcripts using the 5-type framework (Framework, Paradigm Shift, Warning, Diagnosis, Principle). USE WHEN user says 'extract insights', 'bóc insight', 'phân tích transcript', 'tìm insight từ video', 'analyze transcript insights', 'rút insight', 'insight từ transcript', 'extract key points from transcript'.
---

# Insight Extractor

Reads a video transcript and extracts the most valuable insights, categorized by the 5 insight types framework. Outputs a concise summary (<200 words) and a structured insights list — ready for Notion or any content system.

---

## When to Use

- User provides a transcript file path and wants insights extracted
- Called by `trend-researcher` agent after subtitle extraction, before Notion push
- User says "bóc insight", "extract insights", "phân tích transcript"
- User wants key takeaways from a video without reading the full transcript

---

## Input

A transcript file path (plain text `.txt` file).

**How to receive input:**
- Direct file path: `research/youtube/trends/some-video/VIDEO_ID.txt`
- Or raw transcript text pasted by user

---

## Process

### Step 1: Load Reference

Read `references/insight-types.md` to calibrate the 5 insight types and their detection signals.

### Step 2: Read Transcript

Read the full transcript file. Understand the overall topic, structure, and teaching style.

**Determine content type:**
- **Tutorial/How-to** → prioritize Framework insights (step-by-step)
- **Opinion/Commentary** → prioritize Paradigm Shift and Principle insights
- **Cautionary/Mistakes** → prioritize Warning and Diagnosis insights
- **Mixed** → extract across all types

### Step 3: Extract Insights

Scan the transcript for moments matching each insight type's signals (from reference).

**Rules:**
- Maximum **10 insights** per transcript
- Each insight needs: **type**, **title** (one-liner), **explanation** (1-2 sentences)
- For tutorials: collapse step-by-step instructions into a single Framework insight with numbered sub-steps
- Skip filler, intros, CTAs, sponsor segments — focus on substance only
- If a moment could be two types, pick the stronger match
- Preserve the speaker's original phrasing when it's powerful

### Step 4: Write Summary

Write a summary of the transcript in **under 200 words**.

**Summary rules:**
- What is this video about? (1 sentence)
- Who is it for? (1 sentence)
- What are the 2-3 biggest takeaways? (rest of summary)
- Write in Vietnamese if transcript is Vietnamese, English if English
- Be specific — no generic "this video talks about marketing"

### Step 5: Format Output

Produce the final markdown output in this exact structure:

---

## Output Format

```markdown
## Summary

[Under 200 words summary]

## Key Insights

### 1. [Title] — `Framework`
[1-2 sentence explanation]

### 2. [Title] — `Paradigm Shift`
[1-2 sentence explanation]

### 3. [Title] — `Warning`
[1-2 sentence explanation]

...up to 10 insights
```

**Type labels must be one of:** `Framework`, `Paradigm Shift`, `Warning`, `Diagnosis`, `Principle`

---

## Quality Criteria

What makes output GOOD vs BAD:
- **GOOD:** Each insight is specific, actionable, and clearly typed — a reader gets value without watching the video
- **GOOD:** Summary tells you exactly what the video covers and who benefits
- **BAD:** Generic insights like "the speaker talks about marketing strategies"
- **BAD:** Summary that just lists topics without specifics
- **BAD:** More than 10 insights (signal: you're not filtering enough)
- **BAD:** Including filler, self-promotion, or sponsor content as insights

---

## References

- `references/insight-types.md` — The 5 insight types with detection signals and examples. **Load before Step 2.**
