# ai_insurance
# Trợ Lý Bảo Hiểm AI

> Hệ thống chatbot thông minh chuyên sâu về **tư vấn bảo hiểm** và **phát hiện rủi ro**, được xây dựng trên nền tảng mô hình ngôn ngữ lớn (LLM) kết hợp kỹ thuật RAG và Fine-tuning.

---

## Giới thiệu

**Trợ Lý Bảo Hiểm AI** là một hệ thống hỏi đáp tự động được thiết kế đặc biệt cho lĩnh vực bảo hiểm tại Việt Nam. Hệ thống không chỉ tư vấn các gói bảo hiểm mà còn có khả năng **phân tích và phát hiện rủi ro** dựa trên thông tin người dùng cung cấp.

Điểm khác biệt cốt lõi của hệ thống:

- **Fine-tuned chuyên biệt** — Mô hình được huấn luyện lại (LoRA fine-tuning) trên bộ dữ liệu bảo hiểm thực tế, giúp hiểu đúng thuật ngữ chuyên ngành và ngữ cảnh Việt Nam.
- **RAG (Retrieval-Augmented Generation)** — Kết hợp tìm kiếm tài liệu thực tế với sinh ngôn ngữ, đảm bảo câu trả lời chính xác và có căn cứ.
- **Học từ lịch sử hội thoại** — Hệ thống ghi nhớ và học từ các cuộc trò chuyện trước, ngày càng trả lời tốt hơn theo thời gian.

---

## Năng lực chuyên môn

### Tư vấn bảo hiểm
- Bảo hiểm sức khỏe, nhân thọ, xe cộ, tài sản
- Giải thích điều khoản hợp đồng bằng ngôn ngữ đơn giản
- Hỗ trợ quy trình yêu cầu bồi thường

### Phát hiện & đánh giá rủi ro
- Phân tích hồ sơ rủi ro cá nhân / doanh nghiệp
- Nhận diện các yếu tố rủi ro tiềm ẩn từ mô tả của người dùng
- Đề xuất mức bảo hiểm phù hợp với mức độ rủi ro
- Phân tích tài liệu bảo hiểm do người dùng cung cấp (PDF)

---

## Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────┐
│                  Người dùng                      │
│           (Chat UI + Upload PDF)                 │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│               Flask App (app.py)                 │
│         /ask  /upload_pdf  /end_session          │
└──────┬───────────────────────────┬──────────────┘
       │                           │
┌──────▼──────┐           ┌────────▼────────┐
│  RAG Engine │           │ Session Manager │
│  (rag.py)   │           │ (session_       │
│             │           │  manager.py)    │
└──────┬──────┘           └────────┬────────┘
       │                           │
┌──────▼──────────────────────────▼────────────────┐
│                  3 Nguồn dữ liệu                  │
│                                                   │
│  [1] System Vector DB   — Tài liệu bảo hiểm gốc  │
│  [2] Session Vector DB  — Lịch sử hội thoại       │
│  [3] User PDF Store     — PDF người dùng nạp lên  │
└───────────────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────┐
│         LLM: Qwen2.5-1.5B + LoRA Adapter        │
│              Fine-tuned on Insurance Data        │
└─────────────────────────────────────────────────┘
```

---

## Cấu trúc thư mục

```
├── app/
│   ├── app.py                  # Flask server, các route API
│   └── templates/
│       └── index.html          # Giao diện chat
│
├── src/
│   ├── chatbot.py              # Logic chatbot chính
│   ├── rag.py                  # Pipeline RAG (truy xuất + sinh câu trả lời)
│   ├── embedding.py            # Embedding văn bản
│   ├── vector_store.py         # Vector DB hệ thống (chỉ đọc)
│   ├── pdf_processing.py       # Xử lý và chunk file PDF
│   ├── session_manager.py      # Quản lý phiên hội thoại theo từng user
│   ├── session_vector_store.py # Vector DB lịch sử hội thoại
│   └── user_pdf_store.py       # Vector DB tạm cho PDF người dùng
│
├── data/
│   ├── raw/                    # PDF tài liệu bảo hiểm gốc
│   ├── processed/              # Văn bản đã xử lý
│   ├── chunks/                 # Các đoạn văn bản đã chunk
│   ├── vector_db/              # Vector DB hệ thống (không chỉnh sửa)
│   └── sessions/
│       ├── raw/                # Lịch sử hội thoại dạng JSON
│       ├── vector_db/          # Vector DB lịch sử (tự cập nhật)
│       └── temp_uploads/       # PDF người dùng nạp lên (xóa sau phiên)
│
├── models/
│   └── lora/                   # LoRA adapter sau fine-tuning
│
└── notebooks/
    ├── demo.py                 # Demo nhanh
    ├── testbase.py             # Test mô hình gốc
```

---

## Cài đặt & Chạy

### Yêu cầu

- Python 3.10+
- GPU khuyến nghị (CUDA) để chạy mô hình nhanh hơn
- RAM tối thiểu 8GB

### Cài đặt

```bash
# 1. Clone repository
git clone https://github.com/your-username/insurance-chatbot.git
cd insurance-chatbot

# 2. Tạo môi trường ảo
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Cài thư viện
pip install -r requirements.txt
```

### Chuẩn bị dữ liệu

```bash
# Xử lý PDF tài liệu bảo hiểm và tạo vector DB
python notebooks/reset_data.py
```

### Khởi chạy

```bash
python app/app.py
# Mở trình duyệt: http://localhost:5000
```

---

## 🔌 API

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/` | Giao diện chat |
| `POST` | `/ask` | Gửi câu hỏi, nhận câu trả lời |
| `POST` | `/upload_pdf` | Nạp file PDF để phân tích |
| `GET` | `/loaded_files` | Danh sách PDF đã nạp trong phiên |
| `POST` | `/end_session` | Kết thúc phiên, dọn dẹp dữ liệu tạm |

**Ví dụ gọi `/ask`:**
```json
POST /ask
{
  "query": "Bảo hiểm sức khỏe nào phù hợp với người 45 tuổi?"
}
```

---

## Bảo mật dữ liệu

- PDF người dùng nạp lên chỉ tồn tại **trong phiên làm việc** và được xóa hoàn toàn khi phiên kết thúc.
- Lịch sử hội thoại được lưu **theo từng user** và không bị trộn lẫn giữa các tài khoản.
- Vector DB hệ thống (tài liệu gốc) là **chỉ đọc** — không có cơ chế nào ghi đè lên dữ liệu này.

---

## Mô hình & Fine-tuning

| Thành phần | Chi tiết |
|---|---|
| Mô hình gốc | `Qwen/Qwen2.5-1.5B` |
| Phương pháp fine-tuning | LoRA (Low-Rank Adaptation) |
| Dữ liệu huấn luyện | Tài liệu bảo hiểm, hợp đồng, quy tắc bảo hiểm Việt Nam |
| Embedding | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Vector DB | FAISS |

---

## Giấy phép

Dự án được phát triển cho mục đích nghiên cứu và ứng dụng thực tế trong lĩnh vực bảo hiểm.

---

<p align="center">Được xây dựng với bằng Python · Flask · LangChain · FAISS</p>
