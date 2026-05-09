# Prompt Templates for Tony Hoang Tweet Carousel

Templates gởi vào Nano Banana Pro (qua AI33). **Luôn paste text nguyên văn** — không paraphrase.

## Shared header block (copy vào mọi prompt)

```
A modern Twitter/X-style post card, clean white background (#FFFFFF), shot straight-on,
4:5 portrait composition, generous 80-100px margins on all sides.

TOP HEADER SECTION (flush left):
- A circular profile avatar (80x80px equivalent) of a Vietnamese man with short dark
  hair wearing a dark cap, friendly confident expression. MATCH THE PROVIDED REFERENCE
  IMAGE exactly — same face, same look, same cap.
- To the right of avatar: profile name "Tony Hoang Learn AI Automation" in bold black
  sans-serif, followed by a Twitter-blue verified checkmark icon (filled circle with
  white check).
- Below the name: handle "@tranvanhoang.com" in smaller gray text.

Typography: clean sans-serif like Inter or Helvetica Neue. Near-black text #111111.
No watermarks, no logos, no extra UI chrome (no like/retweet buttons, no timestamp).
High resolution, crisp text rendering, professional editorial look.
```

---

## Layout A — Tweet Card Classic

Dùng cho: storytelling, insights, quotes, reasoning.

```
<SHARED HEADER BLOCK>

BODY SECTION (below header, left-aligned, starting ~40px below handle):

Render this exact text verbatim, preserving line breaks, paragraphs, and bold markers.
Bold the words wrapped in **double asterisks** (render bold, not literal asterisks):

<<<
{{SLIDE_BODY_TEXT}}
>>>

Body paragraphs spaced with comfortable line-height (~1.5). Font size large enough to
fill the card width comfortably — approximately 28-32 point equivalent. NO bullets,
NO boxes, NO icons, NO emoji (unless the text above includes them).
```

**Example (VN):**

```
<<<
Bây giờ bạn nghĩ xem...

Bạn tạo MỘT sản phẩm số.

Bạn upload **một lần duy nhất.**

Hệ thống in, đóng gói, giao thẳng tới khách của bạn.

Khách nhận được sản phẩm thật. Bạn rảnh tay xây thêm dòng thu nhập khác.

Học viên của mình đã bán **20.000+ sản phẩm số** và tạo ra **hơn 2 tỷ đồng doanh thu** chỉ với hệ thống này.

Đó là đòn bẩy số thực sự.
>>>
```

---

## Layout B — Prompt Showcase

Dùng cho: actionable prompts, frameworks, công thức.

```
<SHARED HEADER BLOCK>

BODY SECTION (below header):

1. TITLE LINE (bold, ~32pt equivalent, left-aligned):
   "{{PROMPT_TITLE}}"
   Example: "Prompt 1 (Find Winning Niches)" or "Prompt 7 (Scaling Strategy Prompt)"

2. GRAY PROMPT BOX (light gray #F5F5F5 background, rounded corners ~16px,
   padding 24px, full width minus margins, 20px below title):
   Render this text inside the box in medium-dark gray (#444444), regular weight,
   comfortable reading size:
   <<<
   {{PROMPT_CONTENT}}
   >>>

3. "How to use it:" SECTION (starts ~40px below box, left-aligned, black text):
   Label "How to use it:" on its own line, then on a new line:
   <<<
   {{HOW_TO_TEXT}}
   >>>

4. "Result you get:" SECTION (~32px below How-to, left-aligned):
   Label "Result you get:" on its own line, then 3 bullet rows below, each starting
   with a bold green checkmark "✓" (color #22C55E), followed by the bullet text in
   black:
     ✓ {{RESULT_1}}
     ✓ {{RESULT_2}}
     ✓ {{RESULT_3}}

All section labels ("How to use it:", "Result you get:") in regular weight, same
size as body. Checkmarks visibly larger/bolder than the bullet text.
```

**Example (EN):**

```
1. TITLE: "Prompt 1 (Find Winning AI Niches)"

2. BOX: Give me 10 low-competition but high-demand AI automation niches that are
growing fast on YouTube and TikTok. Include target audience, pain points, and why
the niche works in 2026.

3. HOW TO: Paste this into Claude before you plan your content calendar. It helps
you pick a niche where buyers are already searching for solutions.

4. RESULTS:
   ✓ Clear niche direction
   ✓ Audience understanding
   ✓ Higher chance of winning content from day one
```

---

## Vietnamese rendering tips

- Nano Banana Pro render được dấu tiếng Việt đầy đủ (à, á, ạ, ư, ơ, đ...)
- Nếu thấy lỗi dấu: thử render từng slide riêng thay vì batch — đôi khi slide dài bị dồn chữ
- Tránh kết hợp emoji + dấu TV trong 1 câu (model đôi khi confuse)
- Bold **xxx** hoạt động tốt, nhưng underline/italic không reliable — tránh dùng

## Slide 1 (hook) patterns

Slide 1 luôn phải stop-scroll. Các patterns hiệu quả:

| Pattern | Template |
|---------|----------|
| Bold claim | "Tôi đã X trong Y tháng chỉ với Z." |
| Surprising stat | "95% người làm nội dung bỏ qua điều này." |
| Contrarian | "Đừng viết content. Hãy làm cái này trước." |
| Curiosity gap | "3 prompts tôi dùng mỗi ngày để scale AI business." |
| Listicle promise | "7 prompts biến Claude thành ghost writer của bạn." |

## Last slide (CTA) patterns

| Type | Example VN | Example EN |
|------|-----------|------------|
| Follow for more | "Theo dõi @tranvanhoang.com để nhận thêm prompt & framework AI mỗi tuần." | "Follow @tranvanhoang.com for more AI automation playbooks weekly." |
| Save this | "Lưu lại để dùng khi cần. Share cho bạn nào đang build AI business." | "Save this for later. Share with a builder who needs it." |
| Community | "Tham gia AI Freedom Builders — cộng đồng One Person Business with AI." | "Join AI Freedom Builders — the One Person AI Business community." |
