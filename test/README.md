# Kịch bản Kiểm thử & Automation Test (Testing)

Thư mục này quản lý toàn bộ tài liệu kiểm thử thủ công (Manual Test cases) và mã nguồn kiểm thử tự động (Automation tests) của dự án.

## 1. Tổ chức thư mục kiểm thử
- `manual/`: Chứa các file kịch bản kiểm thử bằng Excel hoặc Markdown (ví dụ: `test-cases-auth.md`).
- `integration/`: Chứa các kiểm thử tích hợp (Integration Tests) kiểm tra sự phối hợp giữa nhiều thành phần.
- `e2e/`: Chứa các kiểm thử trải rộng từ đầu đến cuối giao diện (End-to-End Tests) sử dụng Cypress hoặc Playwright.

## 2. Quy tắc viết Test Case
Mỗi test case cần mô tả rõ các trường hợp:
1. **Given (Tiền điều kiện)**: Trạng thái hệ thống trước khi thực hiện test.
2. **When (Hành động)**: Tác động của người dùng hoặc hệ thống.
3. **Then (Kết quả mong đợi)**: Phản hồi mong đợi từ hệ thống.

Ví dụ:
```markdown
### TC-01: Đăng nhập thành công với tài khoản hợp lệ
- **Given**: Tài khoản `test@example.com` đã được kích hoạt trong DB.
- **When**: Nhập đúng Email, Mật khẩu và nhấn nút "Đăng nhập".
- **Then**: Đăng nhập thành công, token được lưu và chuyển hướng đến trang Dashboard.
```

## 3. Khởi chạy Automation Test
### Backend (Pytest)
```bash
pytest
```

### Frontend (Jest / Vitest)
```bash
npm run test
```
