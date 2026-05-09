# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Brand voice — read before producing content

Before generating any marketing content (Facebook posts, Reels / YouTube scripts, captions, CTAs, hooks) or any time you need to understand the user (Hoàng) better — persona, tone, pillars, taboo phrasings — read [brandvoice.md](brandvoice.md) in this repo root first. This applies even when a skill does not explicitly reference it.

## What this repo is

A **distribution bundle** of 17 Claude Code skills + 1 orchestrator agent that apply Brendan Kane's viral content methodology (*One Million Followers*, *Hook Point*, *The Guide to Going Viral*) to writing Facebook posts, Reels scripts, and YouTube scripts. Source: the `hoang-ai-marketing` workspace; exported 2026-04-22 for reuse in other projects.

There is **no code** — only markdown. No build, no tests, no lint. No package manager. Not a git repo.

## Install / distribute

The bundle is consumed by copying into a target project's `.claude/` directory (or `~/.claude/` for global):

```bash
cp -r .claude/skills/mkt-kane-* /path/to/target/.claude/skills/
cp .claude/agents/mkt-brendan-kane-pipeline.md /path/to/target/.claude/agents/
```

## Repository layout

```
.claude/
  skills/mkt-kane-*/           # 17 skills, each self-contained
    SKILL.md                   # frontmatter (name, description, pillar) + prose
    references/*.md            # worked examples the skill pulls from
  agents/mkt-brendan-kane-pipeline.md   # orchestrator
README.md                      # catalog + install instructions
```

Every skill follows the same layout: one `SKILL.md` + a `references/` folder of examples. Preserve that shape when adding a skill.

## Skill categories (see README.md for full table)

- **Research**: `gsb-research-builder`, `viral-format-identifier`, `cross-industry-viral-scout`
- **Ideation**: `eov-reverse-engineer`, `generalist-repackager`
- **Writing — Facebook**: `fb-post-communication-algorithm`, `fb-post-golden-triangle`
- **Writing — Reels**: `reels-jenga-tension`, `reels-untold-stories`, `reels-visual-metaphor`, `reels-is-it-worth-it`
- **Writing — YouTube**: `youtube-jenga-longform`, `youtube-30-day-challenge`
- **Retrofit**: `triple-f-boost`, `cta-non-autocratic-rewriter`, `anti-pattern-auditor`
- **Review**: `gold-comparison-reviewer`

## Orchestrator: `mkt-brendan-kane-pipeline`

9-step pipeline (Research → Format ID → EOV → Repackage → Platform pick → Draft → Audit → Boost → Gold comparison) with **3 hard user approval gates** at steps 3, 5, 9. Artifacts saved to `research/pipeline/[topic-slug]/NN-*.md`. When editing the agent file, do not remove gates, do not remove the loop-back logic at steps 7 and 9, and keep the skill routing table in Step 5 in sync with the skill names in `.claude/skills/`.

## Conventions that matter when editing

- **Frontmatter is load-bearing.** Each `SKILL.md` starts with YAML: `name`, `description`, `pillar`. The orchestrator routes by `name`, and Claude Code triggers skills by keyword-matching `description`. Rename a skill → update the agent's routing table and README.md table at the same time.
- **Output language is Vietnamese** (brand voice "Hoàng" — AI educator VN), with English "power words" kept as-is. To retarget for another brand, edit the Brand voice / Personal voice section inside each `SKILL.md` and keep the framework intact (README.md §Ngôn ngữ output).
- **Pillars P1–P5** (AI Demo, One Person Business, AI News/Trends, Mindset, + one more) are a taxonomy used in `pillar:` frontmatter and in the orchestrator's `FINAL.md`. They refer to the target project's content pillar system — this bundle does not define them.
- **External brand files referenced by skills** (`BRANDVOICE.MD`, `WHO10X TECH.MD`) live in the consuming project, not in this bundle. A skill mentioning them is not broken; the consumer supplies them.
- **Each writing skill enforces its own structural rules** (e.g. Last Dab written first, Feelings+Facts+Fun ≥75%, non-autocratic CTA). When changing one skill, read its `SKILL.md` end-to-end — the rules are specific and scripted.

## When adding a new skill

1. Create `.claude/skills/mkt-kane-<slug>/SKILL.md` with frontmatter: `name`, `description` (include trigger phrases — Claude Code matches on these), `pillar`.
2. Add a `references/` folder with at least one worked example.
3. Register it in `README.md` under the appropriate category.
4. If it should be reachable from the pipeline, add a row to the routing table in `.claude/agents/mkt-brendan-kane-pipeline.md` (Step 5).
