---
name: mkt-youtube-knowledge-script
description: "Viết kịch bản video YouTube dạng chia sẻ kiến thức AI/công nghệ (8-20 phút) bằng tiếng Việt. Hỗ trợ 3 dạng video chính: Listicle (Top N tools), Progression/Roadmap (X cấp độ/bước), Tool Tutorial (vấn đề → giải pháp → demo). Tạo nhiều hook variations theo Kallaway framework để user chọn. Output gồm hook options + full script + hướng dẫn visual/demo. Use this skill whenever users need YouTube video scripts, want to create knowledge-sharing videos about AI tools, tutorials, tech reviews, comparisons, or educational content. Also use when users say 'viết script YouTube', 'kịch bản video dài', 'script chia sẻ kiến thức', 'làm video hướng dẫn', 'video tutorial', 'video review tool', 'video top N', 'video X cấp độ', 'youtube script', 'kịch bản youtube'."
---

# YouTube Knowledge Script Creator

Viết kịch bản video YouTube chia sẻ kiến thức AI/công nghệ (8-20 phút) theo phong cách đã được chứng minh hiệu quả — phân tích từ các creator hàng đầu (Chase AI, Greg Isenberg, Cole Medin) với hàng triệu lượt xem.

**Khán giả**: Người Việt Nam muốn học AI, đa số không có nền tảng kỹ thuật. Viết sao cho học sinh lớp 5 cũng hiểu được.

**Ngôn ngữ output**: TOÀN BỘ bằng tiếng Việt. Giọng tự nhiên, gần gũi như đang nói chuyện với bạn bè — không phải đọc sách giáo khoa.

**Quy tắc ngôn ngữ quan trọng — CHỈ DANH TỪ KỸ THUẬT mới giữ tiếng Anh**:
- Tiếng Anh CHỈ ĐƯỢC dùng cho **danh từ kỹ thuật** không có từ Việt tương đương tự nhiên (API, HTML, JavaScript, open source...)
- **Động từ**: LUÔN dùng tiếng Việt — "lấy dữ liệu" không phải "scrape", "chặn" không phải "block", "vượt qua" không phải "bypass", "nghiên cứu" không phải "research"
- **Tính từ**: LUÔN dùng tiếng Việt — "mạnh" không phải "powerful", "hung hãn" không phải "aggressive"
- **Từ thông dụng có tiếng Việt tự nhiên**: LUÔN dùng tiếng Việt — "tài khoản" không phải "account", "trường hợp tốt nhất" không phải "best case", "hủy" không phải "cancel"
- Lần đầu nhắc danh từ kỹ thuật → kèm giải thích tiếng Việt. Lần sau → dùng thoải mái
- Câu ngắn, từ đơn giản. Đọc to lên phải nghe tự nhiên như đang nói chuyện

**Danh từ kỹ thuật ĐƯỢC giữ tiếng Anh** (dịch ra nghe lạ hơn giữ nguyên):
- Tên riêng: Claude Code, ChatGPT, GitHub, Firecrawl, Docker
- Thuật ngữ nền tảng: API, HTML, JavaScript, markdown, schema, token, bot, open source, CLI
- Tên tính năng/chế độ của tool: scrape, crawl, agent (khi nói về tên action cụ thể, VD: "chế độ scrape")

**PHẢI dùng tiếng Việt** (có từ Việt tự nhiên, dùng tiếng Anh sẽ khó hiểu):

| ❌ Không dùng | ✅ Dùng tiếng Việt |
|--------------|-------------------|
| research | nghiên cứu |
| account | tài khoản |
| block/blocked | chặn/bị chặn |
| bypass | vượt qua |
| cancel | hủy/tắt |
| deploy | triển khai/cài đặt |
| dump | đổ/xả |
| render | hiển thị |
| parse | phân tích/xử lý |
| match | ghép/chọn đúng |
| setup (động từ) | cài đặt |
| trigger | kích hoạt |
| struggle | chật vật/khó khăn |
| aggressive | mạnh/hung hãn |
| powerful | mạnh mẽ |
| best case | trường hợp tốt nhất |
| trade-off | đánh đổi |
| description | mô tả (bên dưới) |
| credit | lượt sử dụng |
| field | trường dữ liệu |
| scale | quy mô lớn |
| update | cập nhật |
| feature | tính năng |
| rating | đánh giá |
| review | bình luận/phản hồi |
| traffic | lượng truy cập |
| source | nguồn |
| lead gen | tìm khách hàng |

**Nguyên tắc vàng**: Nếu bà ngoại bạn nghe mà hiểu → OK. Nếu phải dừng lại suy nghĩ → dùng tiếng Việt.

## Nguyên Tắc Cốt Lõi

### 1. The Dance — But/Therefore (QUAN TRỌNG NHẤT)
Kỹ thuật storytelling cốt lõi: KHÔNG BAO GIỜ nối các phần bằng "rồi sau đó" (and then). LUÔN dùng **"nhưng"** (but) hoặc **"vì vậy"** (therefore) để tạo chuỗi xung đột → giải quyết → xung đột mới.

**Quy tắc bắt buộc:**
- Mỗi phần script PHẢI kết thúc bằng một "nhưng" hoặc "vì vậy" dẫn sang phần tiếp theo
- Không bao giờ có 2 phần liên tiếp mà không có tension (xung đột/bất ngờ) ở giữa
- Khi giải thích xong một khái niệm → ngay lập tức đặt câu hỏi/lo ngại/twist mới trước khi đi tiếp
- Trong phần demo: mỗi bài thử phải escalate (tăng độ khó/bất ngờ), không lặp pattern

**Cách áp dụng vào từng dạng video:**
- **Dạng hướng dẫn**: Vấn đề → NHƯNG có giải pháp → VÌ VẬY hãy xem cách hoạt động → NHƯNG có lo ngại (giá? phức tạp?) → VÌ VẬY mình chạy thử cho xem → NHƯNG bài thử 2 khó hơn → VÌ VẬY rõ ràng tool này đáng dùng → NHƯNG có điều cần biết (hạn chế)
- **Dạng liệt kê**: Item N hay → NHƯNG item N+1 còn hay hơn (escalation) → NHƯNG cái này có bẫy/caveats
- **Dạng cấp độ**: Cấp N dễ → NHƯNG đa số dừng ở đây → VÌ VẬY nếu muốn lên cấp tiếp phải biết trick này → NHƯNG cấp tiếp lại có thách thức mới

**Câu nối But/Therefore mẫu (tiếng Việt):**
- "Nghe hay rồi, **nhưng** chắc bạn đang nghĩ..."
- "Okay, **nhưng** khoan đã — có một vấn đề..."
- "**Vì vậy** rõ ràng rồi đúng không? **Nhưng** bài thử tiếp theo mới thật sự bất ngờ..."
- "**Nhưng** đừng vội mừng — có một điều bạn cần biết..."
- "Và **chính vì vậy** mình sẽ cho bạn xem luôn..."

**Kiểm tra sau khi viết:** Đọc lại toàn bộ script và đánh dấu mỗi chỗ nối giữa các phần. Nếu thấy "and then" (rồi tiếp theo, tiếp theo là, bước tiếp) → viết lại thành But hoặc Therefore.

### 2. Giọng Nói Thật — Không Phải Đọc Bài (QUAN TRỌNG)
Script phải nghe như đang NÓI CHUYỆN, không phải đọc văn bản viết sẵn. Đây là điểm khác biệt giữa script "hay" và script "thật".

**Kỹ thuật bắt buộc:**
- **Filler words tự nhiên**: Rải đều "đúng không?", "thử nghĩ xem", "nói thật nhé", "okay", "à", "ờ" — cứ 3-5 câu phải có 1 filler
- **Tự phản ứng**: Khi nêu số liệu/kết quả, PHẢI có reaction — "Điên đúng không?", "Mình cũng choáng khi thấy con số này", "Nghĩ mà xem — 42 giây!"
- **Tự sửa/bổ sung giữa chừng**: "Firecrawl có 8 khả năng — à thật ra, bạn chỉ cần biết 5 cái thôi" — tạo cảm giác đang nghĩ real-time
- **Câu hỏi tu từ cho viewer**: "Bạn thấy chưa?", "Hình dung được không?", "Có nghe quen không?" — kéo viewer vào cuộc trò chuyện
- **Ngắt nhịp bất ngờ**: Sau câu dài → câu siêu ngắn. "Firecrawl xong trong 42 giây, đầy đủ dữ liệu, không lỗi gì hết. Claude Code bình thường? 5 phút. Và trắng tay."
- **Kể lại trải nghiệm cá nhân**: "Mình thử lần đầu, nói thật là không tin. Nên mình chạy lại lần hai. Vẫn vậy." — không phải đọc spec

**Kiểm tra**: Đọc to script lên. Nếu nghe giống đang thuyết trình → viết lại. Phải nghe giống đang ngồi cà phê kể cho bạn bè nghe.

**Ví dụ so sánh:**
- ❌ Script kiểu đọc bài: "Firecrawl giải quyết vấn đề lấy dữ liệu web của Claude Code một cách hiệu quả, với thời gian xử lý nhanh gấp 7 lần."
- ✅ Script kiểu nói chuyện: "Nói thật nhé — mình chạy xong mà không tin luôn. 42 giây. Claude Code bình thường? 5 phút rưỡi, rồi trắng tay. Điên đúng không?"

### 3. Bằng Chứng Thật — Show The Receipts (QUAN TRỌNG)
Không bao giờ nói chung chung. Mọi tuyên bố PHẢI có bằng chứng cụ thể đi kèm.

**Quy tắc bắt buộc:**
- **Con số cụ thể**: Không nói "nhanh hơn nhiều" → nói "42 giây so với 5 phút 30 giây". Không nói "rất nhiều người dùng" → nói "60.000 lượt yêu thích trên GitHub"
- **Screencast/chạy thử thật**: Mỗi tuyên bố về hiệu suất PHẢI có hướng dẫn quay màn hình kèm theo. Tag `**[QUAY MÀN HÌNH]**` ở mỗi chỗ cần demo thật
- **So sánh trực quan**: Dùng format split-screen (bên trái vs bên phải) cho mọi so sánh. Không chỉ nói — phải CHO XEM
- **Thừa nhận giới hạn**: "Tool này không phù hợp cho [X]" — tạo trust. Đừng bao giờ nói cái gì cũng tốt
- **Nguồn dữ liệu**: Nếu trích số liệu từ nguồn khác, nói rõ: "Theo bài kiểm tra của [nguồn]" hoặc "Mình tự chạy thử và đây là kết quả"
- **Booking.com pattern**: Nếu có thêm demo nhưng kết quả lặp lại → NÓI cho viewer biết rồi CẮT: "Mình còn thử thêm [X] nữa, nhưng kết quả y hệt — nên mình không muốn tốn thời gian của bạn." → Tạo trust bằng cách TÔN TRỌNG thời gian viewer

**Tag demo trong script:**
```
**[QUAY MÀN HÌNH]**: Mô tả chính xác cần quay gì — "Mở Claude Code, gõ [câu lệnh], chờ kết quả, zoom vào [phần cụ thể]"
**[SPLIT SCREEN]**: "Trái: [gì], Phải: [gì]"
**[SỐ LIỆU THẬT]**: "Chạy test thật, ghi lại: thời gian [X], số kết quả [Y], lỗi [Z]"
```

### 4. Chi Tiết Kỹ Thuật Hai Lớp
Script phải phục vụ ĐỒNG THỜI người mới (hiểu được) VÀ người biết code (không thấy nhạt). Dùng kỹ thuật "hai lớp":

**Lớp 1 — Giải thích đời thường (cho tất cả):**
> "Firecrawl lấy dữ liệu và sắp xếp gọn gàng — kiểu như thay vì đưa cả cuốn sách 500 trang, nó tóm tắt thành 2 trang đúng trọng tâm."

**Lớp 2 — Chi tiết kỹ thuật nhanh (cho người biết code):**
> "Cụ thể hơn cho bạn nào muốn biết: nó chuyển HTML thành markdown sạch, và bạn có thể set schema đầu ra — kiểu chỉ lấy product name, price, rating — nên Claude Code không phải đọc 13.000 dòng HTML thô."

**Quy tắc:**
- Lớp 1 LUÔN đi trước — ai cũng hiểu
- Lớp 2 là TÙY CHỌN — chỉ thêm khi có chi tiết kỹ thuật đáng nói
- Dùng câu chuyển: "Cụ thể hơn cho bạn nào tò mò:", "Nói kỹ thuật một chút:", "Cho bạn nào muốn biết sâu hơn:"
- Lớp 2 NGẮN — tối đa 1-2 câu, rồi quay lại dòng chính
- Không phải phần nào cũng cần lớp 2 — chỉ thêm khi tạo giá trị thật sự

**Ví dụ trong script:**
- ❌ Chỉ có lớp 1: "Firecrawl lấy dữ liệu gọn gàng hơn." (người biết code: "Ờ, nhưng cụ thể là gì?")
- ❌ Chỉ có lớp 2: "Firecrawl convert HTML sang markdown với custom JSON schema." (người mới: "Hả?")
- ✅ Hai lớp: "Nó sắp xếp dữ liệu gọn gàng, chỉ lấy đúng cái bạn cần. Nói kỹ thuật một chút — nó chuyển mã nguồn trang web thành dạng văn bản sạch, và bạn có thể chỉ định trước muốn lấy những gì. Nên thay vì 13.000 dòng, Claude Code chỉ cần đọc 10 dòng."

### 5. Mở Đầu Là Sinh Tử
Câu mở đầu quyết định 70% hiệu suất video. Tự chọn **3 loại mở đầu phù hợp nhất**, dùng cái mạnh nhất viết script luôn. Tham khảo [references/hooks-youtube.md](references/hooks-youtube.md) và Kallaway framework (`.claude/skills/mkt-hook-kallaway/SKILL.md`) khi cần.

### 6. Bố Cục Rõ Ràng
Người xem phải biết mình đang ở đâu trong video. Đánh số thứ tự, chia cấp độ, chia bước — tạo cảm giác tiến triển.

### 7. Ngôn Ngữ Đơn Giản Tuyệt Đối
- Viết sao cho học sinh lớp 5 cũng hiểu (ở lớp 1)
- Nếu một câu dài hơn 20 từ → tách làm hai câu
- Dùng phép so sánh quen thuộc: "giống như...", "kiểu như khi bạn..."
- Tránh câu phức, mệnh đề lồng nhau

## Quy Trình Làm Việc

### Bước 1: Thu Thập Thông Tin

Hỏi user nếu thiếu:

1. **Chủ đề chính** — Video nói về gì? (vd: "5 công cụ AI mới nhất")
2. **Dạng video** — Dạng liệt kê / Dạng cấp độ / Dạng hướng dẫn? (gợi ý nếu user không biết)
3. **Đối tượng** — Ai xem? Trình độ nào?
4. **Độ dài mong muốn** — Bao nhiêu phút?
5. **Điểm chính** — Những nội dung cần đề cập?
6. **Kêu gọi hành động** — Muốn người xem làm gì sau khi xem?

### Bước 2: Chọn Dạng Video

Có 3 dạng chính, mỗi dạng có tài liệu tham khảo riêng:

| Dạng | Khi Nào Dùng | Tham khảo |
|------|-------------|-----------|
| **Dạng liệt kê** | Top N công cụ, tài nguyên, mẹo hay | [references/listicle.md](references/listicle.md) |
| **Dạng cấp độ** | X cấp độ, giai đoạn, lộ trình | [references/progression.md](references/progression.md) |
| **Dạng hướng dẫn** | Hướng dẫn công cụ, vấn đề→giải pháp→chạy thử | [references/tool-tutorial.md](references/tool-tutorial.md) |

**Đọc tài liệu tham khảo tương ứng** trước khi viết kịch bản. Tài liệu chứa bản mẫu chi tiết + ví dụ.

### Bước 3: Tự Chọn Top 3 Mở Đầu + Viết Script Luôn

**KHÔNG chờ user chọn.** Tự phân tích nội dung, chọn 3 loại mở đầu phù hợp nhất từ [references/hooks-youtube.md](references/hooks-youtube.md), và viết luôn kịch bản đầy đủ dùng mở đầu #1 (mạnh nhất).

**Cách chọn 3 mở đầu:**
1. Xác định dạng video → tra bảng "Cách Chọn Mở Đầu Phù Hợp" trong hooks-youtube.md
2. Chọn loại mạnh nhất cho dạng đó làm #1 (⭐ Đề xuất — dùng cho script)
3. Chọn 2 loại dự phòng phù hợp với nội dung cụ thể làm #2 và #3

**Trình bày top 3 mở đầu ngắn gọn** (mỗi cái 3-4 dòng), rồi viết script đầy đủ ngay bên dưới:

```
## 🎯 Chủ đề: [mô tả]
**Dạng video**: [Liệt kê / Cấp độ / Hướng dẫn]

### Mở đầu 1: [Loại] — ⭐ DÙNG CHO SCRIPT
**Lời nói**: "[câu nói]"
**Chữ trên màn hình**: "[chữ]"

### Mở đầu 2: [Loại] — Dự phòng
**Lời nói**: "[câu nói]"

### Mở đầu 3: [Loại] — Dự phòng
**Lời nói**: "[câu nói]"

---
[SCRIPT ĐẦY ĐỦ BÊN DƯỚI]
```

### Bước 4: Viết Kịch Bản Đầy Đủ

Viết kịch bản đầy đủ **ngay lập tức** dùng mở đầu #1, theo bản mẫu của dạng video đã chọn (từ tài liệu tham khảo). Không chờ user confirm.

**Định dạng kịch bản:**

```
# [TIÊU ĐỀ VIDEO]

## Thông tin
- Dạng: [Liệt kê / Cấp độ / Hướng dẫn]
- Độ dài ước tính: [X phút]
- Đối tượng: [ai xem]

---

## MỞ ĐẦU (0:00 - 0:15)
[Kịch bản mở đầu đã chọn]
**HÌNH ẢNH**: [mô tả hình ảnh]
**CHỮ TRÊN MÀN HÌNH**: [chữ hiển thị]

## PHẦN 1: [Tên phần] (0:15 - X:XX)
[Kịch bản chi tiết]
**HÌNH ẢNH**: [mô tả hình ảnh/chạy thử cho phần này]
**HÌNH MINH HỌA**: [gợi ý hình ảnh kèm theo]

## QUẢNG CÁO GIỮA VIDEO (X:XX - X:XX)
[Giới thiệu tự nhiên — cộng đồng/khóa học]

## PHẦN 2: [Tên phần]
...

## KẾT + KÊU GỌI HÀNH ĐỘNG (X:XX - X:XX)
[Kêu gọi hành động + tổng kết]
```

### Bước 5: Gợi Ý Tiêu Đề + Ảnh Bìa

Đề xuất 3-5 tiêu đề video theo công thức đã chứng minh:
- Có số cụ thể khi có thể
- Tạo khoảng trống tò mò
- Dưới 60 ký tự

Mô tả ý tưởng ảnh bìa (thumbnail):
- Ý tưởng chính
- Chữ trên ảnh bìa (tối đa 5 từ)
- Biểu cảm/cảm xúc của người trong ảnh

## Quy Tắc Kịch Bản

### Nhịp Độ
- **Mở đầu**: 10-15 giây — gây sốc hoặc tò mò NGAY
- **Lời hứa**: 5-10 giây — nói rõ người xem sẽ được gì
- **Nội dung chính**: Chia thành các đoạn 2-4 phút
- **Quảng cáo giữa video**: Đặt ở ~30-40% video, chuyển tiếp tự nhiên
- **Kết bài**: 30-60 giây, kêu gọi hành động cụ thể

### Chuyển Tiếp Giữa Các Phần
Không bao giờ nhảy đột ngột. Dùng câu nối:
- "Okay, giờ phần tiếp theo mới thật sự hay..."
- "Nhưng khoan đã, cái này mới là thứ thay đổi cuộc chơi..."
- "Và nếu bạn thấy cái đó đã hay, thì cái tiếp theo sẽ khiến bạn choáng..."

### Quảng Cáo Giữa Video (Giới Thiệu Sản Phẩm/Cộng Đồng)
- Đặt SAU khi đã chia sẻ giá trị (không phải đầu video)
- Chuyển tiếp tự nhiên từ nội dung trước đó
- Ngắn gọn (15-30 giây)
- Bản mẫu: "Trước khi mình đi tiếp, nếu bạn đang muốn [lợi ích liên quan đến video], thì cộng đồng AI Freedom Builders là nơi [giá trị]. Link ở mô tả bên dưới."

### Giọng Văn Chuẩn Hoàng
- "mình" cho ngôi thứ nhất, "bạn" / "các bạn" cho người xem
- Tự tin nhưng không quá phấn khích (7/10 năng lượng)
- Keyword tiếng Anh OK khi tự nhiên — kèm giải thích tiếng Việt lần đầu (xem Quy tắc ngôn ngữ ở trên)
- Khái niệm phức tạp → giải thích lớp 1 (đời thường) + lớp 2 tùy chọn (kỹ thuật ngắn)
- Ví dụ: "API — kiểu như ổ cắm điện, giúp hai phần mềm nói chuyện với nhau"
- **Filler words BẮT BUỘC**: "đúng không?", "nói thật nhé", "thử nghĩ xem", "okay", "hình dung được không?" — rải đều cứ 3-5 câu/lần
- **Phản ứng cảm xúc với số liệu**: "Điên đúng không?", "Mình cũng choáng", "Nghĩ mà xem!"
- **Kể trải nghiệm cá nhân**: "Mình thử lần đầu, nói thật là không tin..." — KHÔNG đọc spec

### Cách Giải Thích Thuật Ngữ Trong Script
Khi buộc phải nhắc đến thuật ngữ tiếng Anh, LUÔN giải thích ngay:
- **Lần đầu nhắc**: Lớp 1 (ví dụ đời thường) + Lớp 2 tùy chọn (kỹ thuật 1 câu)
- **Lần sau nhắc**: Có thể dùng lại mà không cần giải thích

Ví dụ trong kịch bản:
- ❌ "Repo này có 60.000 stars trên GitHub"
- ✅ "Kho mã nguồn này trên GitHub — nơi mà lập trình viên chia sẻ code miễn phí — có tới 60.000 lượt yêu thích. Điên đúng không? Mới ra 3 tuần mà đã 60.000."

### Những Điều KHÔNG Làm
- ❌ Mở đầu bằng "Xin chào các bạn" hoặc giới thiệu bản thân
- ❌ Giảng dạy kiểu sách giáo khoa — script phải nghe như NÓI CHUYỆN
- ❌ Hứa hẹn quá mức mà không có bằng chứng cụ thể (số liệu, demo)
- ❌ Đưa quá nhiều khái niệm mà không cho xem thử
- ❌ Kết thúc mờ nhạt — luôn kêu gọi hành động rõ ràng
- ❌ Dùng tiếng Anh khi có thể nói tiếng Việt
- ❌ Dùng thuật ngữ mà không giải thích (thiếu lớp 1)
- ❌ Câu dài, phức tạp, nhiều mệnh đề
- ❌ Nói "nhanh hơn", "tốt hơn" mà không có con số cụ thể
- ❌ Viết script nghe giống đang thuyết trình — phải nghe giống ngồi cà phê kể chuyện
- ❌ Nối phần bằng "and then" — phải dùng But/Therefore (xem Nguyên Tắc #1)
