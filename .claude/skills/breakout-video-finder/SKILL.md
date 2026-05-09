---
name: breakout-video-finder
description: Find breakout YouTube videos with 2x+ view-to-subscriber ratio. USE WHEN user says 'find breakout videos', 'search for breakout video ideas', 'find viral video angles', 'youtube breakout research', 'find videos that overperformed', 'research video ideas for breakout potential', 'find underperforming videos that went viral', 'youtube video opportunity research'.
---

# Breakout Video Finder

Find breakout YouTube videos (videos with 2x+ view-to-subscriber ratio) based on a video idea. This skill researches video opportunities by generating multiple angles, keywords, and finding successful breakout examples.

---

## When to Use

- User provides a video idea and wants to find breakout video examples
- User wants to research video angles before creating content
- User wants to find viral/breakout video patterns in a niche
- User wants to understand what makes videos overperform

---

## Output

**Type:** research
**Location:** `research/youtube/breakout/[video-idea-slug]/`

**Files produced:**
- `breakout-report.md` - Comprehensive report with all findings
- `angles.md` - Core angles and perspective shifts identified
- `keywords.md` - Keywords organized by angle
- `videos.md` - All discovered videos with metrics

---

## Phase-Based Workflow

This skill operates in 4 phases with user approval gates between each phase.

### Phase 1: Generate Core Angles

**Input from user:** A video idea/topic

**Action:**
1. Ask user for the video idea if not provided
2. Generate 5 core angles/perspective shifts for the video idea
3. Present angles to user for approval

**Presentation format:**
```
## Phase 1: Core Angles

For video idea: "[USER'S IDEA]"

### Angle 1: [Title]
[Brief description of the angle]

### Angle 2: [Title]
[Brief description]

... (5 angles total)

---

Please review these angles and let me know:
1. Which angles resonate with you?
2. Should we modify or replace any?
3. Ready to proceed to keyword generation?
```

**Quality criteria for angles:**
- Each angle should be distinctly different from others
- Angles should offer unique perspective shifts
- At least 2 angles should be counter-intuitive or surprising

---

### Phase 2: Generate Keywords

**Trigger:** User approves angles in Phase 1

**Action:**
1. For each approved angle, generate 5 keywords (25 total)
2. Present keywords organized by angle for approval

**Presentation format:**
```
## Phase 2: Keywords by Angle

### Angle 1: [Title]
- Keyword 1
- Keyword 2
- Keyword 3
- Keyword 4
- Keyword 5

### Angle 2: [Title]
- Keyword 1
...

... (all angles)

---

Please review these keywords and let me know:
1. Should we add any keywords?
2. Should we remove any that don't fit?
3. Ready to proceed to YouTube search?
```

**Quality criteria for keywords:**
- Keywords should be searchable on YouTube
- Mix of broad and specific keywords
- Include question-based keywords (how to, what is, why does)
- Include problem/solution keywords

---

### Phase 3: Parallel Sub-Agent Search

**Trigger:** User approves keywords in Phase 2

**Action:**
1. Spawn 5 parallel sub-agents (Task tool), one for each angle's keywords
2. Each sub-agent searches YouTube for videos matching:
   - 5+ minutes duration (no shorts)
   - Focus on finding breakout videos (2x+ view/subscriber ratio)
3. Collect results from all sub-agents

**Search instructions for sub-agents:**
- Search for each keyword in the angle
- Filter for videos 5+ minutes only
- Look for videos with high view-to-subscriber ratios
- Note: Exact subscriber counts may not be available, so prioritize videos with明显 high engagement relative to typical performance
- Return top 5-10 videos per keyword with:
  - Video title
  - Channel name
  - Subscriber count (estimate if needed)
  - View count
  - Duration
  - Estimated breakout score (views/subscribers if available)
  - What makes this video a breakout

**Sub-agent prompt template:**
```
Research YouTube videos for angle: [ANGLE TITLE]
Keywords to search: [KEYWORDS]

Find videos that:
- Are 5+ minutes long (no shorts)
- Show breakout potential (high views relative to channel size)
- Are relevant to: [VIDEO IDEA]

For each video found, capture:
- Title, Channel, Duration
- Estimated views, subscriber count
- Breakout score (if calculable)
- Why it breakout

Return all findings in a structured format.
```

---

### Phase 4: Consolidate Report

**Trigger:** All sub-agents complete their searches

**Action:**
1. Consolidate all findings into a comprehensive report
2. Present summary to user for approval before finalizing

**Presentation format:**
```
## Phase 4: Research Summary

### Total Videos Found: [X]
### Breakout Videos Identified: [X]
### Angles Covered: [X/X]

### Top Breakout Videos by Angle:

#### Angle 1: [Title]
1. [Video Title] - [Channel] - [Breakout Score]
2. ...

#### Angle 2: [Title]
...

---

### Key Patterns Identified:
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]

### Recommendations:
- [Recommendation 1]
- [Recommendation 2]

---

Should I finalize this report? Any adjustments needed?
```

---

## Video Filtering Rules

**CRITICAL - Always enforce:**
- ⛔ EXCLUDE: YouTube Shorts (videos under 5 minutes)
- ✅ INCLUDE: Videos 5+ minutes only
- ✅ PRIORITY: Videos showing breakout potential (2x+ views to subscriber ratio)

**Breakout identification:**
- If subscriber data available: breakout score = views / subscribers
- If not available: look for high engagement signals (high like ratio, comments, shares)
- Prioritize channels where views significantly exceed typical benchmark for their size

---

## User Approval Gates

**Gate 1 (after Phase 1):**
- Present 5 core angles
- Wait for user confirmation before Phase 2
- Allow modifications to angles

**Gate 2 (after Phase 2):**
- Present 25 keywords (5 per angle)
- Wait for user confirmation before Phase 3
- Allow keyword additions/removals

**Gate 3 (after Phase 3):**
- Present research summary
- Wait for user confirmation before final report
- Allow final adjustments

---

## Quality Criteria

**Good output includes:**
- ✅ 5 distinct, non-overlapping angles
- ✅ 25 relevant, searchable keywords
- ✅ Videos only 5+ minutes
- ✅ Focus on breakout/overperforming videos
- ✅ Clear organization by angle
- ✅ Actionable insights and patterns

**Bad output includes:**
- ❌ Generic angles that don't offer new perspectives
- ❌ Keywords too broad or irrelevant
- ❌ Including YouTube Shorts
- ❌ Not prioritizing breakout videos
- ❌ No clear organization
- ❌ Missing video details

---

## Execution Notes

- Always start by asking for the video idea if not provided
- Be explicit about each phase transition and wait for approval
- Use Task tool with subagent_type=general-purpose for parallel searches
- Run sub-agents in parallel for efficiency (all 5 simultaneously)
- Create output directory before writing files
- Follow the user approval gates strictly - do not skip phases
