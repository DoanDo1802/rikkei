# Backend Codebase - MediCore

Thư mục này chứa mã nguồn xử lý logic nghiệp vụ và API của dự án MediCore.

## 1. Công nghệ sử dụng
- **Framework**: FastAPI (Python) - Hiệu năng cao, hỗ trợ bất đồng bộ (async/await)
- **Database ORM**: SQLAlchemy / SQLModel
- **Database**: PostgreSQL (với phần mở rộng PgVector hỗ trợ tìm kiếm RAG)
- **Authentication**: JWT (JSON Web Tokens) với mã hóa mật khẩu bằng bcrypt
- **Real-time**: WebSocket (STOMP protocol) để truyền tin gọi số thứ tự thời gian thực

## 2. Cấu trúc thư mục chi tiết

```text
medicore-backend/
├── app/
│   ├── main.py                     # Entry point khởi chạy ứng dụng FastAPI (tương tự Application.java)
│   │
│   ├── core/                       # Các cấu hình và lớp tiện ích dùng chung (common)
│   │   ├── config.py               # Quản lý biến môi trường (.env), cấu hình Database
│   │   ├── security.py             # JWT token, mã hóa mật khẩu (SecurityConfig.java)
│   │   ├── exceptions.py           # Xử lý lỗi toàn cục tập trung (GlobalExceptionHandler)
│   │   └── websocket.py            # Gateway WebSocket quản lý kết nối real-time (MC-07)
│   │
│   ├── api/v1/                     # TẦNG API (Giao tiếp HTTP - Tương đương controller)
│   │   ├── api.py                  # Điểm tập hợp và khai báo toàn bộ các routers
│   │   └── endpoints/              # Phân chia endpoint theo nghiệp vụ chi tiết
│   │       ├── auth.py             # Đăng ký, đăng nhập & phân quyền (MC-03)
│   │       ├── appointments.py     # Đặt lịch khám, gán lịch tự động (MC-06)
│   │       ├── medical_records.py  # Tạo bệnh án (MC-09) & Tóm tắt bệnh sử (MC-13)
│   │       └── admin.py            # Quản lý lịch trực bác sĩ (MC-04) và danh mục (MC-05)
│   │
│   ├── schemas/                    # TẦNG ĐỊNH NGHĨA DATA (DTO - Data Transfer Object)
│   │   ├── request/                # Validate dữ liệu đầu vào gửi lên từ Frontend (Pydantic models)
│   │   └── response/               # Chuẩn hóa định dạng dữ liệu JSON trả về cho Frontend
│   │
│   ├── models/                     # TẦNG ÁNH XẠ CƠ SỞ DỮ LIỆU (Database Entity)
│   │   ├── base.py                 # Định nghĩa Model cha (chứa id, created_at, updated_at)
│   │   ├── user.py                 # Map với bảng users
│   │   ├── patient.py              # Map với bảng patients
│   │   ├── doctor.py               # Map với bảng doctors
│   │   └── medical_record.py       # Map với bảng medical_records
│   │
│   ├── crud/                       # TẦNG TƯƠNG TÁC DATABASE (Repository / CRUD)
│   │   ├── base.py                 # Các hàm CRUD generic dùng chung (select, insert, update...)
│   │   ├── user.py                 # Xử lý câu lệnh truy vấn bảng users
│   │   ├── patient.py              # Xử lý câu lệnh truy vấn bảng patients
│   │   ├── doctor.py               # Xử lý câu lệnh truy vấn bảng doctors
│   │   └── medical_record.py       # Xử lý câu lệnh truy vấn bảng medical_records
│   │
│   └── services/                   # TẦNG NGHIỆP VỤ (Service Layer / Business Logic)
│       ├── auth.py                 # Logic xử lý đăng ký, tạo mã OTP, phân quyền
│       ├── appointment.py          # Logic tự động phân bổ ca khám (Cân bằng tải Round Robin)
│       ├── medical_record.py       # Logic tạo bệnh án điện tử và lưu trữ
│       ├── ai.py                   # Kết nối LLM (Gemini/OpenAI), thực hiện RAG gợi ý chuyên khoa
│       └── email.py                # Dịch vụ gửi email nhắc lịch tự động, gửi hóa đơn/đơn thuốc
│
├── migrations/                     # Quản lý Database migrations (Alembic)
├── requirements.txt                # Danh sách thư viện Python cần cài đặt
├── .env.example                    # Tệp mẫu hướng dẫn cấu hình biến môi trường
└── README.md                       # Tài liệu hướng dẫn sử dụng backend
```

## 3. Cài đặt & Khởi chạy (Hướng dẫn nhanh)

```bash
# 1. Tạo và kích hoạt môi trường ảo Python
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux

# 2. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 3. Khởi chạy server FastAPI (Local Development)
uvicorn app.main:app --reload
```
