---
name: create-skill
description: Create new skills for Claude Code. USE WHEN user says 'create a skill', 'build a skill', 'make a skill for', 'add a skill', 'new skill for', 'I need a skill that', 'teach claude to', 'make claude do', 'automate [task]'.
---

# Create Skill

Teaches Claude how to create properly structured skills through a guided interview process.

---

## What is a Skill?

A skill is a set of instructions that teaches Claude HOW to do something. Skills live in `.claude/skills/[skill-name]/`.

**Key insight:** Skills make Claude THINK like an expert, not just follow steps.

---

## The 5-Phase Interview Process

When creating a NEW skill, guide the user through these phases:

### Phase 1: UNDERSTAND
Ask the user:
- "What should this skill do?"
- "What problem does it solve?"
- "What's the end result you want?"

**Goal:** Understand the transformation (input → output)

### Phase 2: TRIGGERS
Ask the user:
- "How would you naturally ask for this?"
- "What are different ways someone might request this?"

**Goal:** Capture 5-8 trigger variations for the description. Include:
- Direct requests ("research youtube channel")
- Indirect requests ("find out about this channel")
- Outcome-focused ("I need to know who my competitors are")
- Action verbs ("analyze", "research", "find", "create", "build")

### Phase 3: COMPLEXITY
Ask the user:
- "Is this one focused task or multiple related workflows?"
- "Does it need reference docs, templates, or scripts?"

**Goal:** Determine skill architecture:

| Complexity | Structure | When to Use |
|------------|-----------|-------------|
| **Simple** | Just SKILL.md | Single focused task |
| **Standard** | SKILL.md + workflows/ | Multiple related workflows |
| **Advanced** | SKILL.md + workflows/ + references/ | Needs templates or guides |
| **Full** | SKILL.md + workflows/ + references/ + scripts/ | Needs automation scripts |

### Phase 4: OUTPUT
Ask the user:
- "Does this skill produce files or just answers?"
- If files: "What type of content is it?" (content, research, data, export)
- "Where should outputs live?"

**Goal:** Determine output structure. Follow CLAUDE.md output organization:
| Output Type | Location |
|-------------|----------|
| Content | `content/[type]/[project]/` |
| Research | `research/[topic]/` |
| Data | `data/[source]/` |
| Exports | `exports/[format]/` |

### Phase 5: PROCESS
Ask the user:
- "Walk me through how YOU would do this manually"
- "What are the key steps?"
- "What makes the difference between good and bad output?"

**Goal:** Extract the expertise, not just the steps.

---

## Skill Architecture Options

### Simple Skill (Single Task)

```
.claude/skills/[skill-name]/
└── SKILL.md
```

**When to use:** One focused task, no variations.
**Example:** A skill that formats text in a specific way.

### Standard Skill (Multiple Workflows)

```
.claude/skills/[skill-name]/
├── SKILL.md                 # Router + overview
└── workflows/
    ├── workflow-1.md        # Specific workflow
    └── workflow-2.md        # Another workflow
```

**When to use:** Multiple ways to accomplish related goals.
**Example:** YouTube research skill with "quick scan" vs "deep dive" workflows.

### Advanced Skill (With References)

```
.claude/skills/[skill-name]/
├── SKILL.md                 # Router + overview
├── workflows/
│   ├── workflow-1.md
│   └── workflow-2.md
└── references/
    ├── template.md          # Templates to follow
    └── guide.md             # Reference documentation
```

**When to use:** Needs templates, examples, or detailed guides.
**Example:** Content writing skill with voice guide and format templates.

### Full Skill (With Scripts)

```
.claude/skills/[skill-name]/
├── SKILL.md                 # Router + overview
├── workflows/
│   ├── workflow-1.md
│   └── workflow-2.md
├── references/
│   └── template.md
└── scripts/
    ├── process.py           # Python automation
    └── fetch.py             # Data fetching
```

**When to use:** Needs Python/bash scripts for automation.
**Example:** Publishing skill with scripts to post to social media APIs.

---

## Folder Purposes

| Folder | Purpose | Loaded When |
|--------|---------|-------------|
| **SKILL.md** | Entry point, routing, overview | Skill triggered |
| **workflows/** | Step-by-step instructions for specific tasks | Specific workflow needed |
| **references/** | Templates, guides, examples to follow | Just-in-time during execution |
| **scripts/** | Python/bash automation (NOT loaded as context) | Executed via Bash tool |

**Key difference:**
- `references/` = Loaded into Claude's context (costs tokens)
- `scripts/` = Executed by Claude, not loaded (no token cost)

---

## SKILL.md Template

```markdown
---
name: skill-name
description: What this skill does. USE WHEN user says 'phrase 1', 'phrase 2', 'phrase 3', 'phrase 4', 'phrase 5'.
---

# Skill Name

Brief description of what this skill accomplishes.

---

## Workflow Routing

| Workflow | When to Use |
|----------|-------------|
| `workflows/quick.md` | Fast overview needed |
| `workflows/deep.md` | Full analysis needed |

---

## When to Use

- User says "[trigger 1]"
- User says "[trigger 2]"
- User wants to [outcome]

---

## Output

**Type:** [content/research/data/export]
**Location:** `[path]/[project]/`
**Files produced:**
- `[filename].md` - [description]

---

## Quick Process (if no workflows)

### Step 1: [Action]
[What to do - focus on the THINKING, not just the action]

### Step 2: [Action]
[What to do]

---

## Quality Criteria

What makes output GOOD vs BAD:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

---

## References (if applicable)

- `references/template.md` - Template to follow
- `references/guide.md` - Detailed guidelines

## Scripts (if applicable)

- `scripts/process.py` - Run via: `python .claude/skills/[skill-name]/scripts/process.py`
```

---

## Workflow File Template

Create in `workflows/[workflow-name].md`:

```markdown
# Workflow Name

## Purpose
What this specific workflow accomplishes.

## When to Use
- User says "[specific trigger]"
- Condition that requires this workflow

## Prerequisites
What must exist before starting (files, data, etc.)

## Steps

### Step 1: [Action]
[Detailed instructions - focus on thinking, not just action]

**Why:** [Why this step matters]

### Step 2: [Action]
[Detailed instructions]

### Step 3: [Action]
[Detailed instructions]

## Output
What this workflow produces:
- `[filename]` - [description]

## Quality Check
Before completing, verify:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

---

## Reference File Template

Create in `references/[reference-name].md`:

```markdown
# Reference Name

## Purpose
What this reference provides.

## When to Load
Load this reference when [condition].

---

[Content: templates, examples, guides, etc.]
```

---

## Scripts Folder

Scripts are Python/bash files that Claude EXECUTES (not loads into context).

**Example: scripts/fetch_data.py**
```python
#!/usr/bin/env python3
"""Fetch data from API and save to file."""
import sys
import json

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    # Your implementation
    results = {"query": query, "data": []}
    print(json.dumps(results))

if __name__ == "__main__":
    main()
```

**In SKILL.md, reference like:**
```markdown
## Scripts

To fetch data, run:
```bash
python .claude/skills/my-skill/scripts/fetch_data.py "search query"
```
```

---

## YAML Frontmatter Rules

**Required fields:**
- `name` - Must match folder name, lowercase with hyphens
- `description` - Must include "USE WHEN user says..." with 5-8 trigger phrases

**Optional fields:**
- `allowed-tools` - Pre-approve specific tools
- `model` - Override model (haiku, sonnet, opus)

**Trigger phrase guidelines:**
- Include verb variations (research/analyze/find/look up)
- Include direct and indirect phrasings
- Include outcome-focused requests
- Think: "How would 5 different people ask for this?"

**Example:**
```yaml
---
name: youtube-research
description: Research YouTube videos and channels. USE WHEN user says 'research this video', 'analyze channel', 'youtube research', 'find videos about', 'who is this youtuber', 'look up this channel', 'competitor analysis youtube', 'what videos are performing'.
---
```

---

## Output Folder Setup

If the skill produces files, add this to the skill:

```markdown
## Output

**Type:** research
**Location:** `research/youtube/[channel-or-topic]/`

Before writing output:
1. Create the output directory if it doesn't exist
2. Use descriptive names for the project subfolder
3. Keep all related files in the same folder
```

**Output type examples:**
- YouTube research → `research/youtube/[channel-name]/`
- Blog content → `content/blog/[post-title]/`
- Competitor data → `data/competitors/[competitor-name]/`
- CSV export → `exports/csv/[export-name]/`

---

## Creation Checklist

Before finalizing a skill, verify:

- [ ] Name matches folder name (lowercase, hyphens)
- [ ] Description has 5-8 trigger phrases
- [ ] Trigger phrases cover different ways to ask
- [ ] Correct architecture chosen (simple/standard/advanced/full)
- [ ] Output location follows CLAUDE.md organization
- [ ] Process captures expertise, not just steps
- [ ] Quality criteria defined
- [ ] Workflow routing table (if multiple workflows)
- [ ] References documented (if using references/)
- [ ] Scripts documented with run commands (if using scripts/)

---

## After Creating a Skill

**Update CLAUDE.md routing table** to include the new skill:

```markdown
## Routing

| When you want to... | Load skill |
|---------------------|------------|
| [New skill purpose] | `new-skill-name` |
```

---

## Common Mistakes

1. **Too few triggers** - Include 5-8 variations, not just 2-3
2. **Generic triggers** - "do research" is too vague; "research youtube competitors" is specific
3. **No output structure** - Always define where files go
4. **Steps without thinking** - Capture WHY each step matters
5. **Name mismatch** - Folder name must match `name` in YAML
6. **Wrong architecture** - Don't overcomplicate simple skills; don't underbuild complex ones
7. **Scripts in references** - Scripts go in `scripts/`, not `references/`
8. **Forgetting CLAUDE.md** - Always update routing table after creating skill

---

**Location:** `.claude/skills/[skill-name]/SKILL.md`
