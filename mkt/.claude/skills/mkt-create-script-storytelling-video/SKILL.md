---
name: mkt-create-script-storytelling-video
description: Tạo kịch bản video YouTube hoàn chỉnh end-to-end — từ Title, Intro, Script đến CTA — áp dụng 6 kỹ thuật storytelling Callaway (1B+ views) cộng 3 framework YouTube chuyên sâu (Intro, Title, Script Writing). Hỗ trợ sản xuất video bằng Remotion (React) với title cards, text overlays, transitions, captions. Input là topic + nội dung sơ bộ + persona + brand voice + hook formula (tùy chọn). Output là file .md chứa: title variants, script hoàn chỉnh, report 6 kỹ thuật, intro quality checklist, CTA strategy. Tùy chọn: tạo Remotion project để render video.
---

# YouTube Storytelling Script Creator

Chuyên gia sản xuất video YouTube end-to-end: từ Title → Script storytelling → Intro tối ưu → CTA chuyển đổi → **Video production với Remotion**.

## References

### Storytelling Core
- [6 Kỹ Thuật Storytelling](references/storytelling_techniques.md) – Chi tiết cách áp dụng từng kỹ thuật khi VIẾT script
- [Script Output Template](references/script_template.md) – Format output report

### YouTube Production Frameworks
- [YouTube Intro Framework](references/youtube_intro_framework.md) – TNT strategy, First 5 Seconds, Hook Structure, Content Building Blocks, CTA
- [YouTube Title Framework](references/youtube_title_framework.md) – 3 Core Emotions, Title Templates, Writing Process, A/B Testing
- [YouTube Script Writing Framework](references/youtube_script_framework.md) – Audience Avatar, Research, Hook Writing, Content Development, Quality Control

### Video Production (Remotion)
- [Remotion Video Production](references/remotion_video_production.md) – Setup, components, composition assembly, render workflow
- Tham khảo thêm từ video skill: `.claude/skills/video/references/remotion-setup.md`, `remotion-tips.md`, `captions.md`


---

## Workflow

### Step 1: Thu Thập Input + Đọc References (SONG SONG)

Thực hiện **đồng thời** 2 việc:

**⚡ Song song A — Thu thập input từ user:**

Hỏi user nếu thiếu:

| Input | Bắt buộc | Mô tả |
|-------|----------|-------|
| **Topic** | ✅ | Chủ đề video |
| **Nội dung sơ bộ** | ✅ | Ý chính, thông tin, data, câu chuyện liên quan |
| **Chân dung khách hàng** | ✅ | Ai xem? Đau ở đâu? Mong muốn gì? |
| **Brand Voice** | ✅ | Giọng điệu thương hiệu (ví dụ: chuyên gia nhưng gần gũi) |
| **Công thức Hook** | ⬜ | User cung cấp hoặc dùng formula mặc định từ reference |
| **Độ dài mong muốn** | ⬜ | Short-form (<3 phút) hay long-form (5-15 phút) |

**Audience Avatar (từ YouTube Script Framework):**
- Demographics, Current State, Pain Points
- Knowledge Level, Goals
- Language họ dùng (từ/cụm quen thuộc)
- Họ mất ngủ vì điều gì? Đã thử gì rồi?

**⚡ Song song B — Đọc TẤT CẢ 5 references cùng lúc:**

Đọc song song 5 file sau (dùng parallel tool calls):
1. [references/storytelling_techniques.md](references/storytelling_techniques.md) – 6 kỹ thuật storytelling
2. [references/script_template.md](references/script_template.md) – Format output report
3. [references/youtube_intro_framework.md](references/youtube_intro_framework.md) – Intro & CTA
4. [references/youtube_title_framework.md](references/youtube_title_framework.md) – Title strategy
5. [references/youtube_script_framework.md](references/youtube_script_framework.md) – Script writing

### Step 2: Strategy & Title-First

> Dùng kiến thức từ youtube_title_framework.md (đã đọc ở Step 1).

**A. Xác định 3 yếu tố cốt lõi:**

| # | Yếu tố | Câu hỏi |
|---|--------|---------|
| 1 | Characters | Ai là nhân vật? (viewer, creator, hay người khác) |
| 2 | Concept | Ý tưởng/khái niệm chính là gì? |
| 3 | Stakes | Điều gì at stake? Viewer mất gì nếu không xem? |

**B. Viết 5 Title Variants:**
1. Curiosity + Fear version
2. Curiosity + Desire version
3. Benefits-focused version
4. Time element version
5. Authority angle version

→ Chọn title tốt nhất (≤ 55 ký tự, front-loaded, emotional trigger rõ)

### Step 3: Xây Dựng Nền Tảng Script (CÓ PHẦN SONG SONG)

**⚡ Song song — Thực hiện đồng thời 3 sub-tasks A, C, D:**

**A. Chọn Story Lens (Kỹ thuật #5)**
1. Liệt kê 3+ góc nhìn về topic: common → less common → unique
2. Chọn góc nhìn "category of one" – càng xa mainstream càng tốt
3. Ghi rõ lý do chọn + so sánh với common lenses

**C. Xác định Video Purpose:**
```
Main Transformation:
  From: [trạng thái trước khi xem]
  To: [trạng thái sau khi xem]

Emotional Journey Map:
  [Cảm xúc đầu] → ... → [Cảm xúc cuối] → [Hành động]
```

**D. Chọn/Áp dụng Hook Formula (Kỹ thuật #6)**
1. Nếu user cung cấp hook formula → dùng formula đó
2. Nếu không → chọn từ 5 formula mặc định trong reference
3. Viết kèm gợi ý **Visual Hook** (show while tell)
4. Tạo 2-3 phiên bản hook thay thế

**⏳ Tuần tự — Sau khi A hoàn thành:**

**B. Xác định Direction (Kỹ thuật #4)** ← phụ thuộc Story Lens từ A
1. Viết **Last Dab** (câu cuối) TRƯỚC – phải quotable, memorable, shareable
2. Viết **Hook** (câu đầu) – punchy + indicative of the plot
3. Đảm bảo last line connect/loop lại first line

### Step 4: Viết Script Hoàn Chỉnh

Áp dụng đồng thời 3 kỹ thuật storytelling + Script Writing Framework:

**The Dance (Kỹ thuật #1):**
- Fill phần giữa (giữa hook và last dab) bằng pattern context → conflict
- Dùng "NHƯNG" / "VÌ THẾ" liên kết các beats, KHÔNG dùng "rồi... rồi..."
- Mục tiêu: ≥ 3 conflict loops

**Rhythm (Kỹ thuật #2):**
- Viết mỗi câu 1 dòng riêng
- Xen kẽ câu ngắn (2-5 từ) / trung bình (8-15 từ) / dài (20+ từ)
- Kiểm tra jagged edge: nhìn cạnh phải document = răng cưa
- Sau câu dài → đặt câu ngắn tạo punch

**Tone (Kỹ thuật #3):**
- Điều chỉnh theo Brand Voice của user
- Viết như đang nhắn tin cho bạn thân
- Thêm rhetorical questions, interaction cues
- Dùng ngôn ngữ đời thường phù hợp brand
- **Dễ hiểu cho học sinh lớp 5**: dùng từ đơn giản, câu ngắn gọn, tránh thuật ngữ chuyên môn (nếu bắt buộc dùng thì giải thích ngay bằng ví dụ hoặc so sánh đời thường). Mỗi ý phức tạp cần có ví dụ minh hoạ cụ thể.

**Content Structure (Script Writing Framework):**
- Mỗi main point: Setup → Teaching → Proof
- Engagement techniques: Tension/Resolution, Make Viewers Feel Smart, Story Elements
- Context trước concepts, Examples sau explanations, Proof sau claims

### Step 5: Tối Ưu Intro (First 30 Seconds)

> Dùng kiến thức từ youtube_intro_framework.md (đã đọc ở Step 1).

**A. First 5 Seconds Check:**
- [ ] Câu đầu MATCH title chính xác
- [ ] Visual đầu MATCH thumbnail
- [ ] Credibility được thiết lập ngay

**B. Hook Structure (20-30 giây):**
1. Opening statement (khớp title)
2. Establish credibility
3. Create curiosity gap
4. Show effort/research (input bias)
5. Promise value

**C. Visual Pacing:**
- Đổi visual mỗi 1.5-2 giây
- Pattern interrupts
- B-roll hỗ trợ nội dung nhắc đến

**D. Retention Killer Check:**
- [ ] KHÔNG có long channel plug ở đầu
- [ ] KHÔNG có unnecessary backstory
- [ ] KHÔNG có slow pacing
- [ ] Purpose video rõ ràng ngay
- [ ] Không quá nhiều context trước value

### Step 6: Xuất Report

> Dùng format từ script_template.md (đã đọc ở Step 1).

Tạo file `.md` theo template, bao gồm:
   - Metadata: topic, story lens, khách hàng, brand voice, ngày
   - **Title Variants** (5 versions + chosen + emotion triggers)
   - Script hoàn chỉnh (kèm visual notes)
   - Bảng 6 kỹ thuật đã áp dụng + bằng chứng cụ thể
   - Chi tiết áp dụng từng kỹ thuật
   - **Intro Quality Checklist** (first 5s, hook structure, retention killers)
   - Gợi ý visual & B-roll
   - 2-3 hook thay thế
   - **CTA Strategy** (Link-Curiosity-Promise)

Lưu file tại path user chỉ định, mặc định `storytelling_script.md`

### Step 7: Sản Xuất Video với Remotion (TÙY CHỌN)

> Chỉ thực hiện khi user yêu cầu tạo video. Đọc [references/remotion_video_production.md](references/remotion_video_production.md) trước khi bắt đầu.

**A. Hỏi user về assets:**

| Asset | Bắt buộc | Mô tả |
|-------|----------|-------|
| **Background video/B-roll** | ✅ | File .mp4 cho từng section (hoặc dùng màu nền) |
| **Background music** | ⬜ | File .mp3 nhạc nền (không bản quyền) |
| **Voiceover** | ⬜ | File .mp3/.wav nếu có sẵn recording |
| **Logo** | ⬜ | File .png transparent |
| **Output format** | ⬜ | Horizontal 1920x1080 (mặc định) hay Vertical 1080x1920 |

**B. Setup Remotion project:**

```bash
# Tạo project tại workspace/content/[video-slug]/remotion/
mkdir -p workspace/content/[video-slug]/remotion/src/compositions
mkdir -p workspace/content/[video-slug]/remotion/public
```

1. Tạo `package.json`, `tsconfig.json`, `remotion.config.ts`, `src/index.ts` (theo template trong reference)
2. Copy assets vào `public/`
3. Chạy `npm install`

**C. Tạo compositions từ script:**

Map từng section của script sang Remotion components:

| Script Section | Remotion Component | Thời lượng |
|---------------|-------------------|-----------|
| HOOK | `TitleCard` — text animation lớn + background | 5 giây |
| INTRO | `OffthreadVideo` + `TextOverlay` credibility | 20-30 giây |
| Body Point N | `SectionTransition` (2s) + `OffthreadVideo` + `TextOverlay` key points | Theo script |
| Conflict (NHƯNG/VÌ THẾ) | `ConflictMarker` overlay | 1-2 giây |
| LAST DAB | `TitleCard` — câu kết memorable | 5-10 giây |
| CTA | `OffthreadVideo` + `TextOverlay` Link-Curiosity-Promise | 10-15 giây |

**D. Tính duration:**

```
Tổng frames = (tổng giây các section) × FPS(30)
Trừ đi: transitions overlap (nếu dùng TransitionSeries)
```

**E. Preview & Iterate:**

```bash
npm run dev  # Mở Remotion Studio
```

- Kiểm tra từng section trong Studio
- Verify timing khớp với script
- Kiểm tra visual pacing (thay đổi mỗi 1.5-2 giây trong intro)
- **KHÔNG tự render** — chờ user xác nhận

**F. Render (khi user đồng ý):**

```bash
npx remotion render StorytellingVideo out/video.mp4 --codec h264 --crf 18
```

---

## Mandatory Rules

### Storytelling Core
1. **Luôn viết Last Dab trước** → rồi Hook → rồi fill giữa
2. **≥ 3 conflict loops** trong script, đánh dấu rõ BUT/THEREFORE
3. **Mỗi câu 1 dòng** khi viết, kiểm tra jagged edge
4. **Tone theo Brand Voice** nhưng luôn giữ conversational
5. **Gợi ý Visual Hook** kèm mỗi câu hook
6. **Report ghi rõ bằng chứng** cho mỗi kỹ thuật đã áp dụng
7. **KHÔNG bắt đầu** bằng greeting ("Xin chào"), opaque hook ("Bạn sẽ không tin")
8. **KHÔNG kết thúc** bằng generic CTA ("Hy vọng hữu ích", "Follow nhé")
9. **Ngôn ngữ dễ hiểu lớp 5**: Toàn bộ script phải đủ đơn giản để học sinh lớp 5 đọc hiểu. Không jargon không giải thích, không câu phức lồng nhau, ưu tiên so sánh và ví dụ gần gũi đời thường.

### YouTube Production
10. **Title TRƯỚC Script** — Title đặt kỳ vọng, script deliver
11. **Câu đầu phải match title** — first line = title reworded
12. **5 title variants** — luôn viết 5 versions dùng emotions khác nhau
13. **Title ≤ 55 ký tự** — front-load thông tin quan trọng
14. **Intro ≤ 30 giây** — không quá dài, get to value nhanh
15. **Visual thay đổi mỗi 1.5-2 giây** trong intro
16. **CTA dùng Link-Curiosity-Promise** — không generic

### Remotion Video Production
17. **LUÔN preview trước render** — mở Remotion Studio, kiểm tra từng section, chờ user xác nhận
18. **KHÔNG dùng CSS transitions/animations** — chỉ dùng `useCurrentFrame()` + `interpolate()` + `spring()`
19. **React 18 only** — Remotion 4.x KHÔNG hỗ trợ React 19
20. **`@remotion/media` KHÔNG tồn tại** — dùng `OffthreadVideo` từ core `remotion`
21. **Dùng `staticFile()`** cho mọi asset trong `public/`
22. **Tên file/folder không có space** — dùng hyphen hoặc underscore
23. **Tính duration chính xác** — trừ transition overlap khi dùng TransitionSeries
24. **Step 7 là TÙY CHỌN** — chỉ thực hiện khi user yêu cầu tạo video, không tự động
