# v1 Script Structures

Three structures for Vietnamese short-form video (TikTok / Reels / Shorts). Adapted from `mkt-create-script-short-video/references/templates.md`, with inline `[REF: url]` markers added.

Default structure: **Before-After**. Only pick Three Acts or Action when the content type really calls for them.

---

## 1. Before-After (default)

**Use for:** tool reviews, tips, hacks, listicles, transformations.

```
[HOOK — 3 giây đầu]
<1 trong 4 hook A/B/C/D>
[REF: source_url]

[TRƯỚC — Vấn đề]
- Nêu vấn đề người xem đang gặp, cụ thể + đo được.
- Ảnh hưởng tiêu cực.

[CẦU NỐI — Giải pháp / N điều / quy trình]
- Bước 1 / Điều 1 / Lý do 1: …
  [REF: <asset phù hợp>]
- Bước 2: …
- Bước 3: …

[SAU — Kết quả]
- Kết quả đo lường được.
- Cảm xúc / lợi ích rõ ràng.

[LAST DAB + CTA]
<câu chốt> Comment "Agent" mình gửi bạn link nhóm học Agents miễn phí nhé.
```

---

## 2. Three Acts (Ba Hồi)

**Use for:** personal story with conflict, journey, "mình từng…".

```
[HỒI 1 — MỞ ĐẦU]
- Bối cảnh ban đầu, mình đang làm gì.
[REF: <bối cảnh>]

[HỒI 2 — XUNG ĐỘT]
- Vấn đề xuất hiện.
- Nỗ lực thất bại.
- Căng thẳng leo thang.
[REF: <vấn đề>]

[HỒI 3 — GIẢI QUYẾT]
- Phát hiện / giải pháp.
- Bài học rút ra.

[LAST DAB + CTA]
```

---

## 3. Action

**Use for:** demo, reaction, tension, "thử xem chuyện gì xảy ra nếu…".

```
[MỞ ĐẦU BẰNG HÀNH ĐỘNG]
- Vào thẳng tình huống, không giới thiệu.
[REF: <clip mở màn>]

[TĂNG CƯỜNG HÀNH ĐỘNG]
- Thử 1 → chưa được.
- Thử 2 → vẫn chưa.
- Căng thẳng leo thang.

[HÀNH ĐỘNG GIẢM DẦN]
- Giải quyết.
- Lời khuyên / bài học.

[LAST DAB + CTA]
```

---

## Picking rules

| Content type | Structure |
|--------------|-----------|
| Top N tools / tips / hacks / update features | **Before-After** |
| Mình từng làm X, sai, sửa lại | **Three Acts** |
| Demo thử một thứ mới, phản ứng, thử thách | **Action** |

When in doubt: **Before-After**.

## Brand rules (enforced by caller)

- `mình` (never `tui`, never `tôi`), `bạn` / `các bạn`
- Short spoken sentences
- Specific numbers
- Brand names OK; no other English jargon
- Target word count ≈ `duration_sec × 2.8` (Vietnamese ~170 wpm)
- One `[REF: url]` per supplied reference, placed at the most relevant beat
