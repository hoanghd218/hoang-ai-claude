---
description: Create a KDP coloring book end-to-end (interview → prompts → images → PDF → cover)
argument-hint: [concept description]
allowed-tools: Agent, AskUserQuestion
---

# KDP Coloring Book Creator

Invoke the `kdp-book-creator` agent to handle the full book creation pipeline.

Use the Agent tool to spawn the kdp-book-creator agent (subagent_type: "kdp-book-creator") with this prompt:

```
Create a KDP coloring book end-to-end.
```

If $ARGUMENTS is provided, pass it as the concept:

```
Create a KDP coloring book with this concept: $ARGUMENTS
```

The agent handles everything: interview, planning, image generation, image review & auto-regeneration, PDF assembly, and cover creation.
