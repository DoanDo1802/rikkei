# Thiết kế Cơ sở Dữ liệu & Sơ đồ ERD (Entity Relationship Diagram)

Thư mục này chứa các thiết kế cơ sở dữ liệu và tài liệu liên quan đến cấu trúc dữ liệu của dự án.

## 1. Công cụ thiết kế khuyên dùng
- **dbdiagram.io**: Để viết định nghĩa cơ sở dữ liệu bằng mã DBML và tạo sơ đồ trực quan.
- **Draw.io / Lucidchart**: Vẽ sơ đồ ERD chi tiết.

## 2. Danh sách các file thiết kế
- [ ] `schema.sql`: File script SQL khởi tạo cơ sở dữ liệu.
- [ ] `erd-diagram.png`: Hình ảnh xuất ra của sơ đồ ERD.
- [ ] `db-specs.xlsx`: File đặc tả chi tiết kiểu dữ liệu, khóa ngoại, ràng buộc của từng bảng.

## 3. Quy tắc đặt tên trong DB
- **Tên bảng**: Dạng số nhiều, viết thường, phân tách bằng dấu gạch dưới (ví dụ: `users`, `user_profiles`, `orders`).
- **Tên cột**: Viết thường, snake_case (ví dụ: `created_at`, `phone_number`).
- **Khóa chính**: Luôn đặt tên là `id`.
- **Khóa ngoại**: Tên bảng số ít kết hợp với `_id` (ví dụ: `user_id` liên kết với bảng `users`).
