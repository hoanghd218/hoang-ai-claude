# Quiz Questions Framework — 15-Question Assessment

15 questions in 3 parts: Contact Info → 10 Best Practices (scoring) → 5 Qualifying Questions (sales intel).

---

## Part A: Contact Info (Pre-Quiz)

Captured BEFORE quiz starts. Minimal friction.

| Field | Required | Method |
|-------|----------|--------|
| Name | Yes | Text input |
| Email | Yes | Text input |
| Location | Auto | IP geolocation |
| Phone | No | Optional text input |

**UX Note:** Only name + email as required fields. Phone optional reduces drop-off. Location auto-captured for geographic segmentation.

---

## Part B: 10 Best Practices Questions (Q1-Q10)

These questions generate the score. Each "Yes" / positive answer = points toward 100%.

### Design Rules

- Cover ALL 3 key areas from the value proposition (roughly 3-3-4 split)
- Questions must be answerable Yes/No or on a simple scale
- Each question = one specific best practice the audience SHOULD be doing
- Phrased as "Do you...?" or "Have you...?" or rate statements
- Order: Start easy (warm-up), build to more specific

### Question Format Options

**Format A — Yes/No (simplest)**
```
Bạn có [best practice]?
☐ Có
☐ Không
```

**Format B — Frequency Scale**
```
Bạn [best practice] thường xuyên như thế nào?
☐ Luôn luôn (hàng ngày)
☐ Thường xuyên (vài lần/tuần)
☐ Thỉnh thoảng (vài lần/tháng)
☐ Hiếm khi / Chưa bao giờ
```

**Format C — Agreement Scale**
```
[Statement about best practice]
☐ Hoàn toàn đồng ý
☐ Đồng ý một phần
☐ Không chắc
☐ Không đồng ý
```

### Scoring Logic

| Format | Points |
|--------|--------|
| Yes/No | Yes = 10pts, No = 0pts |
| Frequency | Always = 10, Often = 7, Sometimes = 3, Never = 0 |
| Agreement | Fully = 10, Partly = 7, Unsure = 3, Disagree = 0 |

Total possible: 100 points → expressed as percentage.

### Example: AI Automation Niche

**3 Key Areas:** AI Readiness (Q1-Q3), Automation Foundation (Q4-Q7), System Scalability (Q8-Q10)

**AI Readiness:**
```
Q1: Bạn có sử dụng AI (ChatGPT, Claude, Gemini...) trong công việc hàng ngày?
☐ Có, mỗi ngày  ☐ Vài lần/tuần  ☐ Thỉnh thoảng  ☐ Chưa bao giờ

Q2: Bạn đã có prompt templates cho các tác vụ lặp lại chưa?
☐ Có  ☐ Chưa

Q3: Team của bạn có ai khác cũng đang sử dụng AI tools không?
☐ Có, cả team  ☐ Vài người  ☐ Chỉ mình  ☐ Không ai
```

**Automation Foundation:**
```
Q4: Bạn có sử dụng công cụ automation (Zapier, Make, n8n...) để kết nối các ứng dụng?
☐ Có  ☐ Chưa

Q5: Các tác vụ lặp lại (nhập liệu, gửi email, báo cáo) đã được tự động hoá chưa?
☐ Đa số đã tự động  ☐ Một số  ☐ Rất ít  ☐ Chưa cái nào

Q6: Bạn có workflow được document rõ ràng cho các quy trình quan trọng?
☐ Có, đầy đủ  ☐ Một số  ☐ Không có

Q7: Dữ liệu kinh doanh của bạn có được tập trung ở một nơi (CRM, dashboard...) không?
☐ Có  ☐ Đang xây dựng  ☐ Chưa
```

**System Scalability:**
```
Q8: Nếu khối lượng công việc tăng gấp đôi, hệ thống hiện tại có handle được không?
☐ Hoàn toàn được  ☐ Phần lớn  ☐ Sẽ gặp khó  ☐ Chắc chắn không

Q9: Bạn có đo lường ROI/hiệu quả của các tools đang sử dụng không?
☐ Có, đều đặn  ☐ Thỉnh thoảng  ☐ Chưa bao giờ

Q10: Bạn có kế hoạch / roadmap cho việc ứng dụng AI & Automation trong 6-12 tháng tới?
☐ Có, rõ ràng  ☐ Có ý tưởng nhưng chưa cụ thể  ☐ Chưa có
```

### Example: Marketing Niche

**3 Key Areas:** Lead Generation (Q1-Q3), Conversion (Q4-Q7), Automation (Q8-Q10)

```
Q1: Bạn có hệ thống tạo leads tự động (landing page, quiz, lead magnet)?
Q2: Website có được tối ưu SEO và tốc độ load <3 giây?
Q3: Bạn có chạy paid ads (Facebook, Google) với tracking đầy đủ?
Q4: Tỷ lệ chuyển đổi từ leads → khách hàng có trên 5%?
Q5: Bạn có email sequence tự động cho leads mới?
Q6: Landing page có A/B testing thường xuyên?
Q7: Bạn có retargeting campaign cho leads chưa mua?
Q8: Marketing campaign có được lên lịch và tự động phát?
Q9: Bạn có dashboard theo dõi các metrics quan trọng (CAC, LTV, ROAS)?
Q10: Content marketing có được produce đều đặn (blog, video, social)?
```

---

## Part C: 5 Qualifying Questions (Q11-Q15)

These do NOT affect the score. They qualify the lead for sales.

### Q11: Current Situation

**Purpose:** Segment the lead by stage/role/size.

**Formula:** "Đâu là mô tả phù hợp nhất với tình huống hiện tại của bạn?"

Give 4-5 mutually exclusive options covering the full range of your audience.

**Template:**
```
Đâu là mô tả phù hợp nhất với tình huống hiện tại của bạn?

☐ [Option A — earliest/smallest stage]
☐ [Option B — growing stage]
☐ [Option C — established stage]
☐ [Option D — advanced stage]
☐ [Option E — enterprise/large scale] (optional)
```

**Example (AI Automation):**
```
☐ Nhân viên văn phòng muốn tối ưu công việc cá nhân
☐ Freelancer / Solopreneur đang xây dựng business
☐ Trưởng phòng / Manager muốn số hoá quy trình team
☐ Giám đốc / CEO muốn chuyển đổi số toàn doanh nghiệp
```

### Q12: Desired Outcome (90 Days)

**Purpose:** Understand what's driving their decision RIGHT NOW.

**Formula:** "Kết quả nào bạn muốn đạt được nhất trong 90 ngày tới?"

Give 3-4 outcome options. These should map to your products/services.

**Template:**
```
Kết quả nào bạn muốn đạt được nhất trong 90 ngày tới?

☐ [Outcome A — awareness/learning]
☐ [Outcome B — foundation/setup]
☐ [Outcome C — growth/scaling]
☐ [Outcome D — transformation/complete overhaul]
```

**Example (AI Automation):**
```
☐ Hiểu rõ AI & Automation có thể giúp gì cho công việc
☐ Setup xong hệ thống tự động hoá đầu tiên
☐ Tự động hoá 70%+ công việc lặp lại
☐ Chuyển đổi số toàn bộ doanh nghiệp
```

### Q13: Biggest Obstacle

**Purpose:** Identify their pain point for targeted follow-up.

**Formula:** "Điều gì đang cản trở bạn nhiều nhất?"

Give 3-4 obstacle options. These should be real barriers you've seen.

**Template:**
```
Điều gì đang cản trở bạn nhiều nhất hiện tại?

☐ [Obstacle A — knowledge gap]
☐ [Obstacle B — resource/time constraint]
☐ [Obstacle C — execution/implementation]
☐ [Obstacle D — organizational/people]
```

**Example (AI Automation):**
```
☐ Không biết bắt đầu từ đâu, quá nhiều tools
☐ Không có thời gian để học và setup
☐ Đã thử nhưng không thấy kết quả rõ ràng
☐ Team không sẵn sàng thay đổi cách làm việc
```

### Q14: Preferred Solution

**Purpose:** Gauge budget and commitment level. Each option implies a price range.

**Formula:** "Giải pháp nào phù hợp nhất với bạn?"

Give 3-4 options from cheapest to most expensive.

**Template:**
```
Giải pháp nào phù hợp nhất với bạn hiện tại?

☐ [Option A — self-serve, lowest price] → implies $10-50
☐ [Option B — guided learning, mid price] → implies $100-500
☐ [Option C — coaching/consulting, higher] → implies $500-5,000
☐ [Option D — done-for-you, premium] → implies $5,000-20,000+
```

**Example (AI Automation):**
```
☐ Tự học qua khoá online và tài liệu hướng dẫn
☐ Tham gia workshop / bootcamp có hướng dẫn trực tiếp
☐ Coaching 1-1 với chuyên gia
☐ Thuê chuyên gia setup toàn bộ hệ thống cho mình
```

### Q15: Anything Else (Open Box)

**Purpose:** Capture unexpected intel. People often reveal budget, timeline, urgency.

**Formula:** "Có điều gì khác bạn muốn chia sẻ thêm không?"

**Template:**
```
Có điều gì khác bạn muốn chia sẻ thêm không?
(Tuỳ chọn — nhưng thông tin này giúp mình đưa ra gợi ý chính xác hơn cho bạn)

[Free text box]
```

**What people typically write (gold mine for sales):**
- Budget constraints or deadlines: "Cần triển khai trước Q2"
- Previous experience: "Đã dùng Zapier nhưng chưa hiệu quả"
- Specific pain: "Mỗi ngày mất 3 tiếng nhập liệu Excel"
- Buying signals: "Sẵn sàng đầu tư nếu thấy ROI rõ ràng"
- Urgency: "Sếp yêu cầu phải có giải pháp trong tháng này"

---

## Question Design Best Practices

1. **Progressive disclosure** — Start with easy questions, build to more personal ones
2. **One concept per question** — Don't combine two things in one question
3. **Positive framing** — "Bạn có..." instead of "Bạn chưa..."
4. **Specific, not vague** — "Bạn có sử dụng AI tools hàng ngày?" not "Bạn có quan tâm đến AI?"
5. **Mutually exclusive options** — No overlap between choices
6. **Exhaustive options** — Cover all possible answers
7. **No leading questions** — Don't imply the "right" answer
8. **Mobile-friendly** — Max 4-5 options per question, short text
