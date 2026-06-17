# AI Skills & Prompts (Kỹ năng của AI)

Tài liệu này chứa danh sách các chỉ dẫn kỹ thuật hoặc prompt đặc thù giúp AI phát huy tối đa khả năng phân tích và xử lý mã nguồn của dự án này.

## 1. Kỹ năng Phân tích Logic & Sửa lỗi
- **Khai thác Log**: AI có kỹ năng phân tích sâu stack trace của Python (FastAPI/SQLAlchemy) và error boundary của React để tìm ra vị trí chính xác gây lỗi.
- **Tối ưu truy vấn SQL/ORM**: Có khả năng phát hiện các lỗi truy vấn kinh điển như `N+1 query problem` trong SQLAlchemy/Django ORM và đề xuất giải pháp sử dụng `joinedload` / `selectinload`.

## 2. Kỹ năng Viết Test Case tự động
- Thiết kế các bộ test sử dụng **Pytest** cho backend và **Jest / React Testing Library** cho frontend.
- Tập trung test kiểm thử tích hợp (Integration Test) cho các luồng nghiệp vụ phức tạp như đăng ký -> gửi OTP -> xác nhận -> đăng nhập.
