---
name: mkt-script-storytelling-analyzer
description: Analyze and evaluate video scripts against 6 proven storytelling techniques (The Dance, Rhythm, Tone, Direction, Story Lenses, Hook). Use when reviewing a video script, transcript, or draft to check if it meets storytelling best practices. Input is a script or transcript text. Output is a detailed .md report with checklist, scores (✅/⚠️/❌), and specific improvement suggestions for each criterion.
---

# Script Storytelling Analyzer

Phân tích kịch bản video theo 6 kỹ thuật storytelling đã được chứng minh (framework Callaway – 1B+ views short-form). Xuất report `.md` chi tiết.

## References

- [Storytelling Criteria & Rubric](references/storytelling_criteria.md) – Chi tiết 6 kỹ thuật + rubric chấm điểm ✅/⚠️/❌

---

## Workflow

### Step 1: Nhận Input

Chấp nhận 1 trong các dạng:
- Kịch bản video (text script)
- Transcript video (raw hoặc đã format)
- Draft outline

Nếu input quá ngắn (< 50 từ), yêu cầu bổ sung hoặc ghi chú "không đủ dữ liệu đánh giá".

### Step 2: Đọc Rubric

Đọc [references/storytelling_criteria.md](references/storytelling_criteria.md) để nắm chi tiết 6 tiêu chí đánh giá.

### Step 3: Phân Tích Từng Tiêu Chí

Với mỗi tiêu chí (6 total), thực hiện:

1. **Tìm bằng chứng** – Trích dẫn cụ thể từ script
2. **Đánh giá mức độ** – ✅ Xuất sắc / ⚠️ Cần cải thiện / ❌ Chưa đạt
3. **Giải thích** – Tại sao đạt hoặc chưa đạt
4. **Gợi ý cải thiện** – Cụ thể, actionable
5. **Viết lại mẫu** – Nếu ⚠️ hoặc ❌, viết lại 1-2 đoạn theo đúng kỹ thuật

### Step 4: Xuất Report và lưu vào file .md

Tạo file report `.md` theo format bên dưới. Lưu file tại path do user chỉ định, hoặc mặc định `storytelling_report.md` trong thư mục hiện tại.

---

## Output Format

```markdown
# 📊 Storytelling Script Analysis Report

**Script:** [Tên hoặc mô tả ngắn]
**Ngày phân tích:** [Date]
**Độ dài script:** [X từ]

---

## 🎯 Tổng Quan

| Tiêu Chí | Đánh Giá | Điểm |
|-----------|----------|------|
| 1. The Dance (But/Therefore) | ✅/⚠️/❌ | X/10 |
| 2. Rhythm (Nhịp điệu) | ✅/⚠️/❌ | X/10 |
| 3. Tone (Giọng điệu) | ✅/⚠️/❌ | X/10 |
| 4. Direction (Hướng & Last Dab) | ✅/⚠️/❌ | X/10 |
| 5. Story Lenses (Góc nhìn) | ✅/⚠️/❌ | X/10 |
| 6. The Hook (Câu mở đầu) | ✅/⚠️/❌ | X/10 |
| **TỔNG ĐIỂM** | | **X/60** |

---

## 1. 💃 The Dance (Context ↔ Conflict)

**Đánh giá:** ✅/⚠️/❌ — X/10

**Phân tích:**
[Mô tả cách script sử dụng but/therefore vs and then]

**Bằng chứng từ script:**
> [Trích dẫn đoạn script minh họa]

**Conflict loops tìm thấy:** X loops

**Gợi ý cải thiện:**
- [Gợi ý cụ thể]

**Viết lại mẫu (nếu cần):**
> [Đoạn viết lại]

---

## 2. 🎵 Rhythm (Nhịp điệu câu chữ)

[Tương tự format trên]

---

## 3. 🗣️ Tone (Giọng điệu)

[Tương tự format trên]

---

## 4. 🧭 Direction (Hướng đi & Last Dab)

[Tương tự format trên]

---

## 5. 🔍 Story Lenses (Góc nhìn)

[Tương tự format trên]

---

## 6. 🪝 The Hook (Câu mở đầu)

[Tương tự format trên]

---

## ✅ Checklist Tổng Kết

- [ ] Script có ≥ 3 conflict loops (but/therefore)?
- [ ] Độ dài câu đa dạng (jagged edge)?
- [ ] Giọng conversational (talking WITH, not AT)?
- [ ] Last line memorable & quotable?
- [ ] Góc nhìn unique (category of one)?
- [ ] Hook punchy + indicative trong 3 giây?
- [ ] Có visual hook đi kèm lời nói?

## 🔥 Top 3 Ưu Tiên Cải Thiện

1. [Ưu tiên cao nhất]
2. [Ưu tiên thứ hai]
3. [Ưu tiên thứ ba]
```

---

## Scoring Guidelines

| Tổng Điểm | Xếp Hạng |
|-----------|----------|
| 50-60 | 🏆 **Xuất sắc** – Script storytelling rất mạnh |
| 35-49 | 👍 **Khá tốt** – Vài điểm cần polish |
| 20-34 | ⚠️ **Trung bình** – Cần cải thiện đáng kể |
| 0-19 | ❌ **Yếu** – Cần viết lại phần lớn script |
