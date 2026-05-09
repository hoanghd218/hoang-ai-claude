# Input Format

Accept EITHER a file path (`.md` / `.txt`) OR inline text pasted in the prompt.

## Recommended Markdown Structure

```markdown
## Idea: <short name>
Angle: <the hook / one-line angle>
Key points:
- <point 1>
- <point 2>
- <point 3>
Length: 60s   # optional
Structure: Before-After   # optional — skill auto-picks if omitted
References:
- https://youtu.be/abc — demo clip from Anthropic
- https://i.imgur.com/oldway.png — screenshot stack trace cũ
- https://x.com/xyz/status/123

## Idea: <next one>
...
```

## Minimum Viable Input

Just a title + a few reference links works. The skill fills gaps with judgment:

```
Idea: Claude Code tự fix bug
Refs: https://youtu.be/abc, https://i.imgur.com/x.png
```

## Inline Prompt Input

User can also just paste something like:

> 1) Topic A. Ref: url1, url2
> 2) Topic B. Ref: url3
> 3) Topic C (no refs)

Parse these loosely — split on numbered items or blank lines.

## Parser Rules

1. An "idea block" starts with a line matching `## Idea:` OR a numbered item (`1)`, `1.`, `- `) at col 0.
2. Inside a block, extract URLs with the regex `https?://[^\s)\]]+`.
3. If a URL is followed by ` — <text>` or `  <text>`, treat `<text>` as the note.
4. Deduplicate URLs within an idea (first note wins).
5. If the user did not specify a structure, let the script writer pick one based on content type.

## Output After Parsing

A list of `{title, angle, key_points[], references[{url,note}], length_sec?, structure?}` objects — passed to the script writing step.
