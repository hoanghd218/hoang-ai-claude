---
name: create-command
description: Create slash commands for Claude Code. USE WHEN user says 'create a command', 'make a command', 'add a command', 'new slash command', 'build a command for', 'I need a shortcut for', 'make a quick action', 'automate this action'.
---

# Create Command

Teaches Claude how to create properly structured slash commands through a guided interview process.

---

## What is a Command?

A command is a shortcut you type to trigger an action. Commands live in `.claude/commands/` and are invoked with `/project:[command-name]`.

**Key insight:** Commands are for quick, repeatable actions. Skills are for complex workflows.

**Example:** `/project:status` runs the status command.

---

## The 3-Phase Interview Process

When creating a NEW command, guide the user through these phases:

### Phase 1: ACTION
Ask the user:
- "What action should this command trigger?"
- "What's the end result?"
- "Is this something you'll run often?"

**Goal:** Understand the repeatable action

### Phase 2: ARGUMENTS
Ask the user:
- "Does this command need input from you each time?"
- "What information would you pass to it?"

**Goal:** Determine if `$ARGUMENTS` or `$1, $2` are needed

### Phase 3: TOOLS
Ask the user:
- "What does this command need to do?" (read files, run git, search web, etc.)
- "Should it auto-approve these tools or ask permission?"

**Goal:** Determine `allowed-tools` for smooth execution

---

## Command Structure

Commands are single markdown files:

```
.claude/commands/
├── status.md        → /project:status
├── research.md      → /project:research
└── deploy.md        → /project:deploy
```

**Namespaced commands:**
```
.claude/commands/
└── git/
    ├── status.md    → /project:git:status
    └── sync.md      → /project:git:sync
```

---

## Command Template

```markdown
---
description: What this command does (shown in command menu)
argument-hint: [optional hint for arguments]
allowed-tools: Tool1, Tool2, Tool3
---

Your command instructions here.

Use $ARGUMENTS to access what the user typed after the command.
Use $1, $2, $3 for individual positional arguments.
Use @filename to include file contents.
```

---

## YAML Frontmatter Options

| Field | Required | Purpose |
|-------|----------|---------|
| `description` | Yes | Shown when user types `/project:` - keep it brief |
| `argument-hint` | No | Hint for arguments, e.g., `[video URL]` or `<topic>` |
| `allowed-tools` | No | Auto-approve these tools (no permission prompts) |
| `model` | No | Override model: `haiku`, `sonnet`, `opus` |

---

## Variables

| Variable | What it contains | Example |
|----------|------------------|---------|
| `$ARGUMENTS` | Everything typed after the command | `/project:research AI tools` → `AI tools` |
| `$1`, `$2`, `$3` | Individual positional arguments | `/project:compare file1.md file2.md` → `$1=file1.md`, `$2=file2.md` |
| `@filename` | Include file contents inline | `@CLAUDE.md` embeds the file |
| `` !`command` `` | Embed bash output (context section) | `` !`git status` `` shows current git status |

---

## Allowed Tools

Auto-approve specific tools so Claude doesn't ask permission:

```yaml
allowed-tools: Read, Write, Bash(git:*)
```

**Common patterns:**

| Pattern | What it allows |
|---------|----------------|
| `Read` | Read any file |
| `Write` | Write/create files |
| `Edit` | Edit existing files |
| `Glob` | Search for files by pattern |
| `Grep` | Search file contents |
| `Bash(git:*)` | Git commands only |
| `Bash(npm:*)` | NPM commands only |
| `Bash(python:*)` | Python scripts only |
| `WebSearch` | Web searches |
| `WebFetch` | Fetch web pages |
| `Skill` | Invoke other skills |
| `Task` | Spawn sub-agents |

**Security tip:** Only auto-approve what's needed. More restrictive = safer.

---

## Examples

### Simple Command (No Arguments)

```markdown
---
description: Check git status and recent commits
allowed-tools: Bash(git:*), Read
---

Show me:
1. Current git status
2. Last 5 commits
3. Any uncommitted changes
```

**Usage:** `/project:status`

### Command with Arguments

```markdown
---
description: Research a topic thoroughly
argument-hint: [topic]
allowed-tools: WebSearch, WebFetch, Read
---

Research this topic: $ARGUMENTS

Provide:
- Key concepts explained simply
- Recent developments (2024-2025)
- Practical applications for business
- 3 actionable insights
```

**Usage:** `/project:research AI automation for small business`

### Command with Positional Arguments

```markdown
---
description: Compare two files
argument-hint: [file1] [file2]
allowed-tools: Read
---

Compare these two files:
- File 1: $1
- File 2: $2

Show:
1. Key differences
2. What changed
3. Which is better and why
```

**Usage:** `/project:compare old-version.md new-version.md`

### Command with File Reference

```markdown
---
description: Review code changes against project standards
allowed-tools: Bash(git:*), Read
---

Review the current code changes.

Project standards to follow:
@CLAUDE.md

Focus on:
1. Does it follow our patterns?
2. Any bugs or issues?
3. Suggestions for improvement
```

**Usage:** `/project:review`

### Command with Embedded Bash Context

```markdown
---
description: Smart commit with context
allowed-tools: Bash(git:*)
---

## Current State
- Status: !`git status --short`
- Branch: !`git branch --show-current`
- Recent: !`git log --oneline -3`

Based on the changes above, create a clear commit message and commit.
```

**Usage:** `/project:commit`

### Command that Delegates to Skill

```markdown
---
description: Transform article into social content
argument-hint: [article URL or path]
allowed-tools: Skill, Read, WebFetch
---

Use the `write` skill to transform this article into:
1. Twitter thread
2. LinkedIn post
3. 3 quote posts

Article: $ARGUMENTS
```

**Usage:** `/project:transform https://example.com/article`

---

## Creation Checklist

Before finalizing a command, verify:

- [ ] `description` is brief and clear (shown in menu)
- [ ] `argument-hint` provided if command needs input
- [ ] `allowed-tools` includes only what's needed
- [ ] Instructions are clear and specific
- [ ] Tested with `/project:[command-name]`

---

## When to Use Commands vs Skills

| Use a Command when... | Use a Skill when... |
|-----------------------|---------------------|
| Quick, repeatable action | Complex multi-step workflow |
| Same action, different inputs | Needs interview/discovery |
| "Just do this thing" | "Help me figure out how to..." |
| Single focused task | Multiple possible paths |

**Examples:**
- `/project:status` → Command (quick action)
- "Create a youtube research skill" → Skill (complex, needs setup)

---

## Common Mistakes

1. **No description** - Always include one (it's shown in the menu)
2. **Forgetting $ARGUMENTS** - Use it if you expect user input
3. **Over-permissive tools** - Only auto-approve what's needed
4. **Too complex** - If it needs multiple phases, make it a skill instead
5. **Vague instructions** - Be specific about what Claude should do

---

**Location:** `.claude/commands/[command-name].md`
**Invoke:** `/project:[command-name]`
**Namespaced:** `/project:[folder]:[command-name]`
