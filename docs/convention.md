# Quy tắc phát triển mã nguồn (Coding Conventions) - Dự án MediCore

Tài liệu này định nghĩa các tiêu chuẩn viết code, quy tắc đặt tên, cấu trúc Git và quy trình phát triển nhằm đảm bảo tính đồng nhất, hiệu quả và chất lượng mã nguồn của dự án MediCore (Next.js & FastAPI).

---

## 1. Quy tắc đặt tên (Naming Conventions)

### 1.1. Biến, Hằng số, Hàm & Lớp
- **Frontend (Next.js - TypeScript)**:
  - **Biến & Hàm**: Sử dụng `camelCase`.
    * Ví dụ: `const patientId = "PAT-2026-0001";`, `function getAppointmentDetails() { ... }`
  - **Component & Class**: Sử dụng `PascalCase`.
    * Ví dụ: `const BookingForm = () => { ... }`, `class CustomAuthError extends Error { ... }`
  - **Hằng số (Constants)**: Sử dụng `UPPER_SNAKE_CASE`.
    * Ví dụ: `const DEFAULT_TIME_SLOT = "08:00 - 08:30";`
  - **Kiểu dữ liệu (Types/Interfaces)**: Sử dụng `PascalCase`.
    * Ví dụ: `interface PatientProfileProps { ... }`

- **Backend (FastAPI - Python)**:
  - **Biến, Hàm & Tệp tin**: Sử dụng `snake_case`.
    * Ví dụ: `current_user = get_current_user()`, `def get_medical_record():`
  - **Class (Models, Schemas, Services)**: Sử dụng `PascalCase`.
    * Ví dụ: `class MedicalRecord(BaseModel):`, `class AppointmentService:`
  - **Hằng số (Constants)**: Sử dụng `UPPER_SNAKE_CASE`.
    * Ví dụ: `ALGORITHMS = ["HS256"]`

### 1.2. Thư mục & Tệp tin (Files & Directories)
- **Frontend (Next.js)**:
  - Tên thư mục routing của App Router: Viết thường, phân tách bằng dấu gạch ngang (nếu cần) hoặc Next.js dynamic routing.
    * Ví dụ: `app/patient/booking/`, `app/(auth)/login/`, `app/patient/encounter/[id]/`
  - Tên component và file tiện ích: Sử dụng `camelCase` hoặc `kebab-case` cho file helper, `PascalCase` cho file components.
    * Ví dụ: `components/features/BookingForm.tsx`, `hooks/useWebSocket.ts`, `utils/format-date.ts`
- **Backend (FastAPI)**:
  - Tên thư mục và tệp tin: Luôn sử dụng `snake_case` (Quy định bắt buộc của module Python).
    * Ví dụ: `app/api/v1/endpoints/medical_records.py`, `app/core/security.py`

---

## 2. Quy tắc Cơ sở dữ liệu (PostgreSQL Database Conventions)

- **Tên bảng**: Luôn viết thường, dạng số nhiều và sử dụng `snake_case`.
  * Ví dụ: `users`, `patients`, `medical_records`, `prescriptions`.
- **Tên cột**: Viết thường, `snake_case`.
  * Ví dụ: `patient_code`, `appointment_date`, `created_at`.
- **Khóa chính**: Đặt tên là `id` (Auto-increment INT/BIGINT hoặc UUID).
- **Khóa ngoại**: Tên thực thể số ít kết hợp với `_id` hoặc tên trường định danh liên kết.
  * Ví dụ: `user_id` liên kết với bảng `users`, `patient_id` liên kết với trường `patient_code` của bảng `patients`.

---

## 3. Quy tắc Git & Commit

### 3.1. Git Branching Model
Chúng ta áp dụng mô hình Git Flow rút gọn:
- `main`: Nhánh chạy production ổn định.
- `develop`: Nhánh tích hợp chính phục vụ kiểm thử (Staging).
- `feature/[mã-task]-[tên-task]`: Nhánh phát triển tính năng mới.
  * Ví dụ: `feature/MC-03-jwt-auth`, `feature/MC-06-patient-booking`
- `bugfix/[mã-task]-[tên-lỗi]`: Nhánh sửa lỗi phát sinh khi test.
  * Ví dụ: `bugfix/MC-08-realtime-queue-delay`
- `hotfix/[tên-lỗi]`: Nhánh sửa lỗi khẩn cấp trực tiếp trên production.

### 3.2. Commit Message Format
Định dạng tin nhắn commit bắt buộc phải kèm mã Backlog (`MC-XX`):
`[Loại] [Mã-Backlog] Mô tả ngắn gọn tính năng/sửa đổi`

Các loại commit (`type`) hợp lệ:
- `feat`: Tính năng mới (Feature)
- `fix`: Sửa lỗi (Bug fix)
- `docs`: Cập nhật tài liệu (Documentation)
- `style`: Định dạng code (không ảnh hưởng logic: khoảng trắng, dấu `;`...)
- `refactor`: Tái cấu trúc mã nguồn (Refactor)
- `test`: Thêm hoặc sửa đổi các bộ test
- `chore`: Các tác vụ cấu hình hệ thống, cài thư viện...

Ví dụ commit hợp lệ:
- `[feat] [MC-03] Thiết kế giao diện Form Đăng ký và validate số điện thoại`
- `[fix] [MC-08] Sửa lỗi WebSocket mất kết nối khi chuyển trang Dashboard`
- `[docs] [MC-01] Cập nhật hình ảnh sơ đồ ERD mới nhất vào README`

thành viên dùng

# Lấy code mới nhất
git checkout develop
git pull origin develop

# Tạo task mới
git checkout -b feature/task-name

# Commit
git add .
git commit -m "Add feature"

# Push
git push origin feature/task-name

# Tạo Pull Request lên develop

---

## 4. Định dạng mã nguồn (Linting & Formatting)

### 4.1. Frontend (Next.js - TypeScript)
- Sử dụng **ESLint** để bắt lỗi cú pháp và **Prettier** để tự động format code.
- Cấu hình thụt lề: **2 spaces** (khoảng trắng).
- Luôn sử dụng dấu chấm phẩy `;` ở cuối dòng lệnh.
- Ràng buộc pre-commit qua **Husky** để đảm bảo code không có lỗi lint trước khi commit.

### 4.2. Backend (FastAPI - Python)
- Sử dụng **Black** hoặc **Ruff** để kiểm tra và định dạng mã nguồn Python.
- Tuân thủ nghiêm ngặt tiêu chuẩn **PEP 8**.
- Cấu hình thụt lề: **4 spaces** (khoảng trắng).
- Không để các thư viện không sử dụng (unused imports) trong code.
