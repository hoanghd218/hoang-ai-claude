
---
name: create-hook
description: Create hooks for Claude Code automation. USE WHEN user says 'create a hook', 'add a hook', 'automate when', 'trigger when', 'run automatically', 'after I save', 'before I commit', 'when file changes'.
---

# Create Hook

Teaches Claude how to create automation hooks that trigger on specific events.

---

## What is a Hook?

A hook is automation that runs when something happens. Hooks live in `.claude/settings.json`.

**Key insight:** Hooks make Claude proactive, not just reactive.

---

## The 3-Phase Interview Process

When creating a NEW hook, guide the user through these phases:

### Phase 1: TRIGGER
Ask the user:
- "When should this run?" (after writing a file, before a command, when session ends, etc.)
- "Should it run for all files or specific ones?"

**Goal:** Identify the event and matcher

### Phase 2: ACTION
Ask the user:
- "What should happen when triggered?"
- "Should Claude think about it (prompt) or run a command (command)?"

**Goal:** Determine hook type and action

### Phase 3: CONFIGURE
- Add the hook to settings.json
- Test it works

---

## Hook Events

| Event | When It Fires | Common Use |
|-------|---------------|------------|
| `PreToolUse` | Before a tool runs | Validate, confirm dangerous actions |
| `PostToolUse` | After a tool runs | Lint, format, organize files |
| `Stop` | Claude stops responding | Session summary, reminders |
| `SubagentStop` | An agent completes | Process agent results |
| `UserPromptSubmit` | User sends message | Input validation |

---

## Hook Types

### Prompt Hooks (Claude thinks)
Claude evaluates the prompt and decides what to do:

```json
{
  "type": "prompt",
  "prompt": "If a file was created in the wrong location, suggest moving it."
}
```

**Use when:** You need Claude's judgment

### Command Hooks (Run script)
Runs a bash command automatically:

```json
{
  "type": "command",
  "command": "npm run lint --fix"
}
```

**Use when:** You want a specific command to run

---

## Matchers

Matchers filter which tools trigger the hook:

| Matcher | What It Matches |
|---------|-----------------|
| `Write` | Only Write tool |
| `Write\|Edit` | Write OR Edit tools |
| `Bash` | Any Bash command |
| `Bash(git:*)` | Only git commands |
| `.*` | All tools (use carefully) |

---

## settings.json Structure

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Your instruction here"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Summarize what was accomplished"
          }
        ]
      }
    ]
  }
}
```

---

## Examples

### Auto-update CLAUDE.md when skill created
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "prompt",
    "prompt": "Check if a skill was just created or renamed in .claude/skills/. If so, update the CLAUDE.md routing table to include it."
  }]
}
```

### Enforce output organization
```json
{
  "matcher": "Write",
  "hooks": [{
    "type": "prompt",
    "prompt": "If a file was just created in the project root, suggest moving it to the appropriate folder (content/, research/, data/, exports/)."
  }]
}
```

### Lint on save
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "npm run lint --fix"
  }]
}
```

### Session summary
```json
{
  "hooks": [{
    "type": "prompt",
    "prompt": "Summarize what was accomplished this session in 2-3 bullet points."
  }]
}
```
*(Note: Stop hooks don't use matchers)*

### Git commit reminder
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "prompt",
    "prompt": "If 5+ files have been modified, remind the user to commit their changes."
  }]
}
```

### Dangerous command warning
```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "prompt",
    "prompt": "Check if this command could delete files or make irreversible changes. If so, warn the user."
  }]
}
```

---

## Quick Setup Flow

When user wants to create a hook:

1. **Identify the event** - When should it trigger?
2. **Choose hook type** - Prompt (Claude thinks) or Command (run script)?
3. **Write the hook** - Add to settings.json
4. **Test it** - Trigger the event and verify it works

---

## Creation Checklist

Before finalizing a hook, verify:

- [ ] Correct event chosen (PostToolUse, PreToolUse, Stop, etc.)
- [ ] Matcher is specific enough (avoid `.*` unless needed)
- [ ] Hook type matches the need (prompt vs command)
- [ ] Prompt is clear and actionable
- [ ] Tested by triggering the event

---

## Common Mistakes

1. **Too broad matcher** - `.*` triggers on everything, use specific matchers
2. **Wrong event** - PostToolUse for after, PreToolUse for before
3. **Vague prompt** - Be specific about what Claude should do
4. **Forgetting Stop hooks don't have matchers** - They just fire when Claude stops
5. **Not testing** - Always trigger the hook to verify it works

---

**Location:** `.claude/settings.json` → `hooks` section
**Events:** PreToolUse, PostToolUse, Stop, SubagentStop, UserPromptSubmit
