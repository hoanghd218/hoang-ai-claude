# Dạng Tool Tutorial — "Problem → Solution → Demo"

Video hướng dẫn một tool/technique cụ thể. Mở bằng pain point, giới thiệu solution, demo thực tế so sánh. Hiệu quả vì viewer đến với nhu cầu cụ thể và muốn thấy kết quả trước khi invest thời gian.

## Khi Nào Dùng

- Hướng dẫn setup/sử dụng một tool cụ thể
- "Claude Code + Firecrawl: Hướng dẫn từ A-Z"
- "Cách dùng MCP server để Claude Code làm mọi thứ"
- "Setup AI Agent tự động hóa email marketing"
- So sánh tool mới vs cách cũ

## Cấu Trúc Template

### HOOK (0:00 - 0:15)
Mở bằng PAIN trực tiếp + solution tease:
- Nêu rõ cái gì KHÔNG hoạt động
- Liệt kê 2-3 problems cụ thể (nhanh, như bullet)
- "Nhưng nếu dùng [tool], tất cả problems này giải quyết dễ dàng"

**Pattern tham khảo (Chase AI — Firecrawl):**
> "Claude code sucks at web scraping. It can't handle anti-bot protections. It struggles with JavaScript heavy sites and half the time it will come back with nothing at all. But if we bring in a tool like Firecrawl, we can solve all of these problems very easily."

**Phân tích cấu trúc:**
1. Bold problem statement — "sucks at X" gây chú ý ngay
2. Liệt kê 3 pain points cụ thể — viewer gật đầu "đúng rồi"
3. "But if we..." — pivot sang solution
4. "Very easily" — hứa không phức tạp

### WHY IT MATTERS (0:15 - 1:00)
Giải thích TẠI SAO viewer nên quan tâm — kết thúc bằng **BUT** dẫn vào phần tiếp:
- Use cases thực tế (2-3 ví dụ)
- Ai sẽ được lợi
- Hậu quả nếu không giải quyết

```
"Vậy tại sao bạn nên quan tâm? Vì có RẤT nhiều việc giá trị cao
cần khả năng này. Ví dụ [use case 1], [use case 2], [use case 3].
Nếu mình bảo Claude Code [task], nó sẽ struggle.
→ VÌ VẬY mình cần giải quyết vấn đề này. NHƯNG giải quyết bằng cách nào?"
```

### HOW IT WORKS (1:00 - 3:00)
Giải thích cơ chế — kết thúc bằng **BUT** (lo ngại giá/phức tạp):
- Overview high-level trước
- So sánh với cách cũ
- Nếu có nhiều features/modes, liệt kê ngắn

```
"Okay, vậy [tool] hoạt động thế nào? Đơn giản lắm.
[Giải thích 2-3 câu].
Cái hay ở đây là [key benefit].
→ NHƯNG chắc bạn đang nghĩ: 'Nghe hay, nhưng tốn bao nhiêu tiền?'"
```

**Nếu tool có nhiều actions/features:**
```
| Action | Khi Nào Dùng | Mức Độ |
|--------|-------------|--------|
| [action 1] | [use case] | Cơ bản |
| [action 2] | [use case] | Nâng cao |
| [action 3] | [use case] | Pro |
```

### PRICING/COST (nếu có) (3:00 - 3:30)
Trả lời lo ngại giá — kết thúc bằng **THEREFORE** (vì vậy cài luôn):
- Nêu trung thực: free plan, paid plans
- Mention open-source alternative nếu có

```
"Tin vui: [giá hợp lý / có bản miễn phí].
→ VÌ VẬY không có lý do gì để không thử. NHƯNG cài đặt có khó không?"
```

### SETUP (3:30 - 5:00)
Trả lời lo ngại setup — kết thúc bằng **THEREFORE** (xong rồi, demo luôn):
- Ngắn gọn, đi thẳng vào
- "Cách dễ nhất là [method]"
- Mention gotchas/lỗi phổ biến

```
"Cài đặt thì 60 giây là xong. [Step 1], rồi [step 2].
NHƯNG có một bước nhiều người hay quên: [gotcha].
VÌ VẬY giờ mọi thứ đã sẵn sàng — nhưng nói suông thì chưa đủ.
Mình cần cho bạn xem kết quả thật."
```

### MID-ROLL CTA (~30-40% video)
Đặt SAU phần setup, TRƯỚC demo — dùng **BUT** để tạo anticipation:

```
"Okay, trước khi mình chạy thử cho bạn xem, nếu bạn đang muốn [benefit]...
[product/community] là nơi [value prop].
Link ở [location]. Giờ vào phần hay nhất — NHƯNG kết quả có thể khiến bạn bất ngờ..."
```

### DEMO / TESTS (5:00 - END-2:00)
Phần quan trọng nhất — phải SHOW, không chỉ TELL.

**Format demo so sánh (Side-by-Side):**
```
## TEST [N]: [Mô tả test]

### Setup Test
- Bên trái: [tool mới]
- Bên phải: [cách cũ / không có tool]
- Task: "[mô tả task cụ thể]"
- Tại sao test này: "[vì website này có X challenge]"

### Kết Quả
- [Tool mới]: [thời gian], [kết quả]
- [Cách cũ]: [thời gian], [kết quả/lỗi]
**VISUAL**: Split screen recording

### Phân Tích
- "[Tool mới] hoàn thành trong [time] vs [cách cũ] mất [time]"
- Highlight sự khác biệt rõ ràng
```

**Số lượng tests**: 2-3 tests là đủ. PHẢI escalate (tăng độ khó + bất ngờ) — KHÔNG lặp pattern:
- Test 1: Basic use case → tool mới thắng rõ ràng (thiết lập kỳ vọng)
- Test 2: Harder scenario → cách cũ fail hoàn toàn, tool mới vẫn ổn (escalation)
- Test 3: **TWIST** → cách cũ CÓ làm được **NHƯNG** chênh lệch vẫn lớn (bất ngờ — phá pattern)

**But/Therefore giữa các demo (BẮT BUỘC):**
- Sau test 1: "Rõ ràng rồi. **Nhưng** đấy mới là trang đơn giản. Nếu trang web có hàng rào chống bot thì sao?"
- Sau test 2: "Okay, vậy trang nào chặn bot thì xong. **Nhưng** nếu trang KHÔNG chặn bot — Claude Code bình thường có đuổi kịp không?"
- Sau test 3: "**Vì vậy** ngay cả khi không bị chặn, vẫn nhanh gấp [N] lần. Câu trả lời rõ ràng rồi."

**Mỗi test phải cho viewer lý do xem test tiếp** — không để họ nghĩ "mình đã biết kết quả rồi."

### BONUS: OPEN SOURCE / ALTERNATIVES (nếu có) (1-2 phút)
- Mention giải pháp thay thế
- Trung thực về trade-offs: "Bạn sẽ mất [X] nhưng được [Y]"
- "Nếu bạn biết Docker, có thể thử route này"

### WRAP UP + CTA CUỐI (30-60s)
- Recap 1-2 câu: "Vậy [tool] giải quyết [problem] cực kỳ hiệu quả"
- Nhắc use case mạnh nhất
- CTA: "Comment cho mình biết bạn sẽ dùng [tool] cho gì"

## Ví Dụ Tiêu Đề Hiệu Quả

- "Claude Code + Firecrawl: Web Scraping Từ 5 Phút Còn 42 Giây"
- "Tool AI Này Thay Đổi Hoàn Toàn Cách Mình Làm [Task] — Hướng Dẫn Đầy Đủ"
- "Mình Đã Thử [Tool] và Kết Quả Khiến Mình Choáng"

## Tips

- **Demo > Giải thích**: Nếu phải chọn giữa giải thích thêm vs demo thêm, luôn chọn demo
- **Side-by-side comparison** là format demo mạnh nhất — viewer thấy ngay sự khác biệt
- **Acknowledge limitations**: "Tool này không phù hợp cho [X]" — tạo trust
- **"The answer is pretty clear"** — confirm kết luận sau demo, đừng để viewer tự đoán
- **Thời lượng**: Tool đơn giản = 8-12 phút, tool phức tạp = 15-20 phút
