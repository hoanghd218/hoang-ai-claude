# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KDP Coloring Book Generator — end-to-end pipeline for producing Amazon Kindle Direct Publishing coloring books (adults + kids). A book flows: `ideas/*.md` → plan (SEO metadata + page prompts) → images (via pluggable renderer) → interior PDF → full-color cover → KDP pre-flight QC. The repo is both a Python toolbox in [scripts/](scripts/) and an orchestration layer of [.claude/agents/](.claude/agents/) + [.claude/skills/](.claude/skills/) that drive those scripts through the `/kdp-create-book` slash command.

## Running the pipeline

All Python entry points live in [scripts/](scripts/). Run from the repo root:

```bash
pip install -r requirements.txt
# .env holds: IMAGE_RENDERER (ai33|bimai|kie|nanopic), *_KEY / *_API_KEY / *_ACCESS_TOKEN,
#             AUTHOR_FIRST_NAME, AUTHOR_LAST_NAME. Never committed.

# Single book (manual, from repo root):
python scripts/plan_book.py --concept "cozy cats in a cafe" --audience adults --pages 30 --theme-key cozy_cat_cafe
python scripts/generate_images.py --plan output/cozy_cat_cafe/plan.json --count 30
python scripts/build_pdf.py      --theme cozy_cat_cafe --author "BoBo Art"
python scripts/generate_cover.py --theme cozy_cat_cafe --author "BoBo Art"
python scripts/pdf_qc.py         --pdf output/cozy_cat_cafe/interior.pdf --trim 8.5x11 --require-even-pages

# Batch (scan output/ for books in known states):
python scripts/batch_generate_images.py [--book <theme_key>] [--ai33-only|--nanopic-only] [--dry-run]
python scripts/batch_rebuild_interior.py             # rebuild every interior.pdf
python scripts/batch_rebuild_cover.py [renderer] [--regenerate]   # default renderer=nanopic; reuses saved front_artwork.png unless --regenerate

# End-to-end via agent orchestrator (preferred):
/kdp-create-book "concept here"           # interviews, plans, generates, reviews, assembles
/kdp-batch-planner                        # one plan per ideas/*.md
/kdp-batch-assembler                      # generate+assemble every book that has plan.json but no interior.pdf
```

`scripts/` is also on `sys.path` for cross-script imports (e.g., `batch_rebuild_*.py` import `build_pdf` / `generate_cover` directly — they are libraries as well as CLIs).

## Architecture

### Data layout
Everything about a single book lives under `output/{theme_key}/`:
```
output/{theme_key}/
  plan.json          — SEO metadata (title/subtitle/description/keywords/categories) + cover_prompt + page_prompts[] + page_size + audience
  prompts.txt        — page prompts, one per line (compat with legacy theme-based flow)
  images/page_NN.png — grayscale line art at 300 DPI
  front_artwork.png  — saved cover front art (reused on rebuild unless --regenerate)
  interior.pdf       — KDP interior upload
  cover.png / cover.pdf — full wrap cover (front + spine + back)
```

Briefs to turn into plans live in [ideas/](ideas/) as markdown with YAML frontmatter (`topic`, `audience`, `style`, `season`, `score`, `status`). Processed ideas move to `ideas/done/`.

### Config modules (two of them — different concerns)

- [scripts/config.py](scripts/config.py) — **runtime** config for the image pipeline: page dimensions, DPI, safe area, per-renderer aspect ratios, renderer URLs/poll timeouts, Gemini model, path helpers (`get_book_dir` / `get_plan_path` / `get_images_dir` / `get_interior_pdf_path` / `get_cover_png_path` / `get_cover_pdf_path`), and `BASE_PROMPT` template. Supports two trim sizes: `8.5x11` (portrait, 3:4) and `8.5x8.5` (square, 1:1). `get_gutter_margin(page_count)` returns the KDP-required inside margin — it grows with page count (0.375" at 24p, 0.5" at 151p, up to 0.875" at 701p+).

  **Important**: `config.THEMES` is a `_ThemesProxy`, not a static dict. It auto-discovers any `output/{theme_key}/plan.json` (or legacy `prompts.txt`) at access time. You do **not** need to register new themes anywhere — `plan_book.py` writing to `output/{theme_key}/` is sufficient for `build_pdf.py` / `generate_cover.py` / `generate_images.py --theme` to see it. (The old CLAUDE.md said otherwise; that hasn't been true since `THEMES` was proxified.)

- [scripts/kdp_config.py](scripts/kdp_config.py) — **domain math**, used by agents and the DB layer. No I/O, no config loading. Contains: `spine_width_inches()` / `full_cover_dims()` with KDP bleed + live area, `printing_cost_usd()` / `royalty_per_sale_usd()` / `break_even_acos_pct()` / `max_cpc_usd()`, `bsr_to_daily_sales()` + `estimate_monthly_royalty()`, `opportunity_score()` / `competition_strength()` / `niche_score()` / `apply_hard_elimination()` (Blue Ocean niche framework), `LIMITS` (title/keyword/DPI caps), `SEASONS` ramp calendar. Keep cover math and royalty rates here; never duplicate into scripts.

### Image generation

[scripts/image_providers.py](scripts/image_providers.py) is the renderer abstraction. `generate_image(prompt, renderer=..., aspect_ratio=...)` dispatches to one of: `ai33`, `bimai`, `kie`, `nanopic`. Default renderer comes from `IMAGE_RENDERER` in `.env`. Each backend polls its own task API (interval + timeout in `config.py`). NanoPic supports a comma-separated `NANOPIC_ACCESS_TOKEN` pool rotated round-robin via a thread-safe singleton (`NanoPickTokenPool`) — `batch_generate_images.py` defaults workers to `tokens × 3`.

[scripts/generate_images.py](scripts/generate_images.py) post-processes every returned image to grayscale, enforces contrast/brightness, fits into the page's safe area with `ImageOps.contain` (preserves aspect), centers on a white page at 300 DPI. Parallelism uses `ThreadPoolExecutor(MAX_PARALLEL_WORKERS=6)`. `--start N` skips existing `page_NN.png`, so reruns are resumable.

[scripts/batch_generate_images.py](scripts/batch_generate_images.py) is the fleet-level version: scans `output/` for books whose `plan.json` has more pages than `images/` contains, then runs two provider pools concurrently (`nanopic` + `ai33` by default, overridable with `--*-only`). `--dry-run` reports gaps without generating. Use this to catch up after provider outages rather than re-running per-book.

### PDF assembly

[scripts/build_pdf.py](scripts/build_pdf.py) assembles the interior in this order: title page → copyright page → coloring pages (odd pages with blank backs) → thank-you page. It forces an even page count (KDP requirement), sets the author consistently across title + copyright (metadata must match the cover), and uses the inside/outside margins from `get_page_dims(size, page_count=N)` so the gutter scales with page count. `--size` picks 8.5x11 or 8.5x8.5; defaults to `plan.json.page_size` when available.

[scripts/generate_cover.py](scripts/generate_cover.py) builds a full wrap cover: calls the renderer for front artwork, then composites spine + back with Pillow text overlay. `full_cover_dims()` from `kdp_config.py` computes spine width from page count (0.002252"/page white paper) + 0.125" bleed on all four sides. `--kdp-width`/`--kdp-height` overrides the calculated wrap size with the exact values KDP shows in the upload dialog. `--regenerate` forces a new AI front; otherwise `front_artwork.png` is reused, which matters for reproducibility.

[scripts/pdf_qc.py](scripts/pdf_qc.py) is the pre-flight validator. Checks trim size, bleed (cover), even page count, and minimum line weight against KDP manual-review rules. Exits non-zero on any CRITICAL violation — wire it into any batch flow that ends in "ready to upload."

### Agent/skill layer

The slash command `/kdp-create-book` (see [.claude/commands/kdp-create-book.md](.claude/commands/kdp-create-book.md)) spawns the `kdp-book-creator` agent, which orchestrates sub-agents: `kdp-plan-writer` → `kdp-image-worker` (generate → review via `kdp-image-reviewer` skill → auto-regen loop) → `kdp-assembly-worker` (build_pdf + generate_cover + pdf_qc). Two batch-level agents — `kdp-batch-planner` (ideas → plans) and `kdp-batch-assembler` (plans → books) — are the right entry points when the user says "plan all ideas" / "batch build". Skills under [.claude/skills/](.claude/skills/) are invoked by name and include `kdp-prompt-writer`, `kdp-image-generator`, `kdp-image-reviewer`, `kdp-book-builder`, `kdp-cover-creator`, `kdp-cover-checker`, `kdp-book-detail` (listing SEO), plus upstream research/analytics skills (`niche-hunter`, `performance-analyst`, `ads-manager`, `quality-reviewer`).

### Database (multi-agent state)

[scripts/db.py](scripts/db.py) is a SQLite CLI at `data/kdp.db` used as the shared state store for the eight-agent system (niches, books, manuscripts, covers, listings, qa_reports, ad_campaigns, royalties, actions, pipelines). Agents that need to persist across conversations should go through this CLI (`python scripts/db.py <resource> <verb> ...`) rather than ad-hoc JSON files.

## KDP rules to honour

Images: 300 DPI min. Interior: grayscale, 0.25" outside margins, page-count-aware gutter (`get_gutter_margin`), even page count, max 4 consecutive blank body pages / 10 trailing. Line thickness ≥ 0.75pt (0.01"); fonts ≥ 7pt; gray fills ≥ 10% coverage. No crop marks, bookmarks, annotations, or encryption; flatten transparency; ≤ 650 MB. **Metadata must match exactly** across title page, copyright, cover, and spine — the #1 rejection cause. Spine text requires ≥ 79 pages (`MIN_SPINE_FOR_TEXT_IN = 0.125`); `full_cover_dims()` returns `spine_can_have_text` — respect it. Banned terms in metadata: "spiral bound", "leather bound", "hard bound", "calendar". Publishing limit: 10 titles per format per week.

Prompt style — adults: cute-cozy medium-detail, layered foreground/midground/background, large stylized shapes, kawaii proportions, NO dense small clusters. Kids 6-12: bold thick clean outlines, single centered subject, NO shading/gradients/borders/frames. Every page prompt must include the "no border / no enclosing rectangle / no frame" clause — the image models love to draw one otherwise.

## Conventions

- Theme keys: `^[a-z][a-z0-9_]*$` (snake_case) — validated in `plan_book.py`. The theme_key is the folder under `output/` and the single ID for a book.
- `generate_images.py --start N` resumes from page N+1 (skips existing files) — safe to re-run after partial failures.
- `build_pdf.py` / `generate_cover.py` reuse the page size from `plan.json` when available; `--size` is an explicit override.
- Cover builds reuse `front_artwork.png` by default; pass `--regenerate` to pay the renderer call again.
- `batch_rebuild_cover.py` runs 6 books in parallel; first positional arg is renderer, second can be `--regenerate`.
- [AGENTS.md](AGENTS.md) is the operator-facing brief (Vietnamese + English) — update it only if the user-visible `/kdp-create-book` flow changes.
