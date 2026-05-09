# Brendan Kane Content System — Skill Bundle for Claude Code

Bundle gồm **17 skills + 1 agent orchestrator** áp dụng phương pháp Brendan Kane (tác giả *One Million Followers*, *Hook Point*, *The Guide to Going Viral*) cho content creation — viết bài Facebook, script Reels, script YouTube theo format đã được chứng minh viral.

## Cài đặt

Copy vào `.claude/` của project:

```bash
# Skills
cp -r skills/mkt-kane-* ~/path/to/your-project/.claude/skills/

# Agent orchestrator
cp agents/mkt-brendan-kane-pipeline.md ~/path/to/your-project/.claude/agents/
```

Hoặc copy vào global: `~/.claude/skills/` và `~/.claude/agents/`

## 17 Skills — phân loại theo mục đích

### 🎯 Research & Identification (3 skills)
| Skill | Dùng khi |
|---|---|
| `mkt-kane-viral-format-identifier` | Phân biệt Viral Format (lâu dài) vs Trend (nhất thời) từ 1 video/post |
| `mkt-kane-gsb-research-builder` | Build Gold-Silver-Bronze sheet so sánh video top/trung bình/thấp của 1 creator |
| `mkt-kane-cross-industry-viral-scout` | Tìm format ngành khác (bác sĩ, luật sư, BDS, thủ công) để apply blue-ocean cho niche của bạn |

### ✍️ Writing — Facebook Post (2 skills)
| Skill | Format |
|---|---|
| `mkt-kane-fb-post-communication-algorithm` | Blend Feelings 30% + Facts 25% + Fun 20% — reach 85% audience |
| `mkt-kane-fb-post-golden-triangle` | Personal Story + Evidence/Data + Timeless Wisdom (mindset posts) |

### 🎬 Writing — Reels 30-90s (4 skills)
| Skill | Signature của creator nào |
|---|---|
| `mkt-kane-reels-jenga-tension` | Mark Rober / Veritasium — stacked micro-questions |
| `mkt-kane-reels-untold-stories` | Daniel Wall — behind-the-scenes "Oh wait, what?!" reveal |
| `mkt-kane-reels-visual-metaphor` | Dr. Julie Smith — 1 physical prop minh hoạ concept trừu tượng |
| `mkt-kane-reels-is-it-worth-it` | Tanner Leatherstein — deconstruct 1 product để verdict value vs price |

### 📺 Writing — YouTube Long-form (2 skills)
| Skill | Signature |
|---|---|
| `mkt-kane-youtube-jenga-longform` | Mark Rober / Veritasium 10-20 phút — teaser + main question + 2 attempts + breakthrough |
| `mkt-kane-youtube-30-day-challenge` | Matt d'Avella — 30-day self-improvement documentary format |

### 🔧 Retrofit & Optimize (4 skills)
| Skill | Dùng khi content đã có |
|---|---|
| `mkt-kane-triple-f-boost` | Viết lại post/script để đạt Feelings+Facts+Fun ≥75% |
| `mkt-kane-generalist-repackager` | Repackage niche topic (tech/AI) thành hook mass appeal |
| `mkt-kane-cta-non-autocratic-rewriter` | Đổi CTA "Mua ngay!" sang Democratic/Benevolent/Laissez-faire |
| `mkt-kane-anti-pattern-auditor` | Phát hiện 4 downward drivers (over-branding, over-production, stock, standardized) |

### 🏆 Review & Compare (1 skill)
| Skill | Dùng khi |
|---|---|
| `mkt-kane-gold-comparison-reviewer` | So sánh side-by-side draft của bạn vs 1 Gold reference theo 8 performance drivers |

## Agent Orchestrator (1)

| Agent | Pipeline |
|---|---|
| `mkt-brendan-kane-pipeline` | End-to-end viral content pipeline cho 1 topic: research → format identify → EOV → repackage → draft (FB/Reels/YouTube) → audit → boost → CTA rewrite → Gold comparison. 9 bước với 3 user approval gate. |

## Thứ tự dùng (workflow chuẩn)

```
1. Research      → gsb-research-builder / viral-format-identifier
2. Ideation      → cross-industry-viral-scout
3. Draft         → fb-post-golden-triangle / reels-* / youtube-*
4. Audit         → anti-pattern-auditor
5. Optimize      → triple-f-boost / cta-non-autocratic-rewriter
6. Final review  → gold-comparison-reviewer
```

Hoặc dùng 1 lệnh: **agent `mkt-brendan-kane-pipeline`** tự chạy toàn bộ.

## Nguồn tham khảo

Source material:
- Sách: *One Million Followers* (Brendan Kane)
- Sách: *Hook Point* (Brendan Kane)
- Sách: *The Guide to Going Viral* (Brendan Kane)
- Podcast: The Futur (Chris Do) × Brendan Kane — "20 Brutal Truths of Social Media"

## Ngôn ngữ output

Các skill này viết content bằng **tiếng Việt** (brand voice "Hoàng" — AI educator VN). Nếu bạn muốn dùng cho brand khác:

1. Edit file `SKILL.md` trong mỗi skill
2. Sửa phần "Brand voice" / "Personal voice" theo persona của bạn
3. Giữ nguyên framework & process

## Requirement

- Claude Code CLI (latest)
- Không cần API keys bổ sung cho các skill này
- Có thể dùng trong bất kỳ project nào (skill-level)

---

**Bundle được export ngày**: 2026-04-22
**Nguồn**: hoang-ai-marketing workspace
**License**: Dùng nội bộ, không redistribute thương mại
