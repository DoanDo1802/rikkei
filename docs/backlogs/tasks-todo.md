# DANH SÁCH NHIỆM VỤ DỰ ÁN MEDICORE (TODO LIST)

Tài liệu này tổng hợp toàn bộ các đầu việc (tasks) cần lập trình và cấu hình cho dự án MediCore, được phân vai cụ thể cho từng thành viên. Bạn có thể sử dụng các ô tích `[ ]` để đánh dấu `[x]` sau khi hoàn thành.

---

## 🛠️ Sprint 1: Nền tảng & Bảo mật (Foundation)

### MC-01: Thiết kế sơ đồ thực thể (ERD) và khởi tạo DB
- [ ] Phân tích các thực thể chính trong hệ thống (Users, Patients, Doctors, Specialties, Appointments, MedicalRecords, Prescriptions, Medicines, Diseases, PrescriptionDetails). - **(Thành viên A)**
- [ ] Thiết kế sơ đồ ERD chi tiết (khoá chính, khoá ngoại, kiểu dữ liệu chuẩn y khoa). - **(Thành viên A)**
- [ ] Viết Script SQL khởi tạo cấu trúc bảng trên PostgreSQL. - **(Thành viên A)**
- [ ] Thiết lập Trigger/Function tự động cập nhật trường `created_at` và `updated_at`. - **(Thành viên A)**
- [ ] Khởi chạy và kiểm tra việc kết nối cơ sở dữ liệu. - **(Thành viên A)**

### MC-02: Thiết lập cấu trúc dự án
- [ ] **Backend**: Khởi tạo môi trường ảo Python, cài đặt FastAPI, Uvicorn, SQLAlchemy/SQLModel. - **(Thành viên A)**
- [ ] **Backend**: Thiết lập cấu trúc phân lớp (`app/api`, `app/core`, `app/models`, `app/schemas`, `app/crud`, `app/services`). - **(Thành viên A)**
- [ ] **Frontend**: Khởi tạo dự án Next.js (App Router), cài đặt Ant Design, Tailwind CSS, Axios, Zustand. - **(Thành viên C)**
- [ ] **Kết nối**: Cấu hình CORS Middleware trong file `main.py` của Backend để cho phép kết nối từ Frontend Next.js. - **(Thành viên A)**
- [ ] **Kiểm tra**: Viết API `/health-check` và gọi thử từ Frontend để kiểm tra đường truyền. - **(Thành viên A)**

### MC-15: Hệ thống định danh kép (Mã Bệnh nhân & Mã Bệnh án)
- [ ] Viết Service sinh mã Bệnh nhân trọn đời: `PAT-YYYY-NNNN` (ví dụ: `PAT-2026-0001`). - **(Thành viên B)**
- [ ] Viết Service sinh mã Bệnh án theo từng ca khám: `EMR-YYYYMMDD-NN` (ví dụ: `EMR-20260616-01`). - **(Thành viên B)**
- [ ] Ràng buộc kiểm tra tính duy nhất (Unique) của mã định danh trên cơ sở dữ liệu. - **(Thành viên A)**

### MC-03: Xác thực và Phân quyền Người dùng (JWT)
- [ ] Xây dựng APIs: Đăng ký tài khoản, Đăng nhập, Đăng xuất (Backend). - **(Thành viên B)**
- [ ] Thiết lập mã hóa mật khẩu người dùng bằng thư viện `bcrypt` (Backend). - **(Thành viên B)**
- [ ] Xây dựng JWT Token Generator & Validator với phân quyền Role (Backend). - **(Thành viên B)**
- [ ] **[Anti-Spam]** Kiểm tra trùng lặp Số điện thoại / Email trước khi cho phép đăng ký. - **(Thành viên B)**
- [ ] Thiết kế giao diện màn hình Đăng nhập & Đăng ký (Frontend). - **(Thành viên D)**
- [ ] Cấu hình Route Guard bảo vệ các trang Dashboard trên Frontend (Next.js Middleware). - **(Thành viên D)**

---

## 📅 Sprint 2: Quản trị & Đặt lịch (Core Flow - Part 1)

### MC-04: Quản lý Bác sĩ, Chuyên khoa và Lịch trực
- [ ] Viết API CRUD cho Chuyên khoa (Specialties) và Bác sĩ (Doctors) (Backend). - **(Thành viên A)**
- [ ] Viết API thiết lập ca trực và lịch làm việc của Bác sĩ (Schedules) (Backend). - **(Thành viên A)**
- [ ] Thiết kế giao diện Admin thêm mới bác sĩ, gán chuyên khoa và phòng khám (Frontend). - **(Thành viên C)**
- [ ] Thiết kế giao diện Admin quản lý Lịch trực theo tuần của từng bác sĩ (Frontend). - **(Thành viên C)**
- [ ] Thêm tính năng "Vô hiệu hóa" tài khoản bác sĩ (không hiển thị trên trang đặt lịch). - **(Thành viên A & C)**

### MC-05: Quản lý Thuốc và danh mục ICD-10
- [ ] Viết API CRUD cho danh mục Thuốc (Medicines) và mã bệnh quốc tế (Diseases - ICD-10) (Backend). - **(Thành viên A)**
- [ ] Xây dựng tính năng Import dữ liệu hàng loạt từ file CSV/Excel cho cả Thuốc và ICD-10 (Backend). - **(Thành viên B)**
- [ ] Thiết kế màn hình Admin quản lý danh sách Thuốc và tìm kiếm mã ICD-10 (Frontend). - **(Thành viên C)**

### MC-06: Đặt lịch khám trực tuyến (Patient Booking)
- [ ] Thiết kế giao diện Bệnh nhân chọn Chuyên khoa -> chọn Bác sĩ -> chọn khung giờ còn trống (Frontend). - **(Thành viên D)**
- [ ] Viết API kiểm tra và trả về các khung giờ (Time Slots) khả dụng của bác sĩ trong ngày (Backend). - **(Thành viên B)**
- [ ] Xây dựng thuật toán cân bằng tải (Round Robin hoặc Random) gán bác sĩ khi bệnh nhân đặt lịch theo Chuyên khoa mà không chọn đích danh bác sĩ. - **(Thành viên B)**
- [ ] **[Anti-Spam]** Viết logic giới hạn: Một bệnh nhân tối đa chỉ được có 2 lịch hẹn ở trạng thái `WAITING`. - **(Thành viên B)**
- [ ] Gửi thông báo đặt lịch thành công về Frontend qua WebSocket. - **(Thành viên B)**

---

## 🩺 Sprint 3: Nghiệp vụ Bác sĩ & Real-time (Core Flow - Part 2)

### MC-07: Thiết lập WebSocket Gateway
- [ ] Cấu hình WebSocket Server sử dụng STOMP protocol (Backend). - **(Thành viên B)**
- [ ] Thiết lập WebSocket Client kết nối tự động khi đăng nhập (Frontend). - **(Thành viên D)**
- [ ] Xây dựng cơ chế tự động kết nối lại (Auto-reconnect) khi mạng yếu. - **(Thành viên D)**

### MC-08: Hàng chờ khám Real-time (Doctor)
- [ ] Thiết kế Dashboard hàng chờ gọi số của phòng khám của Bác sĩ (Frontend). - **(Thành viên D)**
- [ ] Kết nối WebSocket tự động đẩy bệnh nhân mới đặt lịch vào hàng chờ mà không cần reload trang (Real-time). - **(Thành viên D)**
- [ ] Cập nhật trạng thái hàng chờ: WAITING -> IN_PROGRESS -> DONE. - **(Thành viên D)**

### MC-09: Thực hiện Khám bệnh & Ghi bệnh án
- [ ] Thiết kế màn hình Thăm khám lâm sàng của Bác sĩ (Frontend). - **(Thành viên C)**
- [ ] Tích hợp tính năng Tìm kiếm mã bệnh ICD-10 hỗ trợ Debounce Search để giảm tải API. - **(Thành viên C)**
- [ ] Viết API lưu trữ Bệnh án điện tử (EMR) vào DB (Backend). - **(Thành viên A)**
- [ ] Ràng buộc bảo mật: Bệnh án sau khi bấm "Hoàn thành" sẽ ở chế độ Read-only (không cho phép sửa). - **(Thành viên A)**

---

## 🤖 Sprint 4: Trí tuệ Nhân tạo & Hoàn thiện (Polishing)

### MC-10: Kê đơn thuốc điện tử & Xuất PDF
- [ ] Thiết kế form Kê đơn thuốc (chọn thuốc, nhập liều dùng, số lượng) đính kèm ca khám (Frontend). - **(Thành viên D)**
- [ ] Viết Service sinh file PDF đơn thuốc tự động có đầy đủ chữ ký, logo phòng khám (Backend). - **(Thành viên B)**
- [ ] Trả link tải đơn thuốc PDF ngay trên giao diện khám của Bác sĩ và hồ sơ Bệnh nhân. - **(Thành viên B & D)**

### MC-11: Cổng thông tin Bệnh nhân (Timeline)
- [ ] Thiết kế giao diện "Hồ sơ sức khỏe" của bệnh nhân dưới dạng Timeline lịch sử (Frontend). - **(Thành viên D)**
- [ ] Viết API kết xuất lịch sử khám bệnh và đường link tải đơn thuốc PDF cũ (Backend). - **(Thành viên D)**

### MC-12: Trợ lý AI Bệnh nhân (Gợi ý chuyên khoa)
- [ ] Thiết kế giao diện khung chat "Trợ lý AI sức khỏe" (Frontend Next.js). - **(Thành viên D)**
- [ ] Xây dựng Prompt và kết nối OpenAI/Gemini phân tích triệu chứng bệnh nhân nhập để gợi ý khoa khám phù hợp (Backend). - **(Thành viên B)**
- [ ] Thêm dòng cảnh báo y khoa miễn trừ trách nhiệm dưới khung chat. - **(Thành viên D)**

### MC-13: Trợ lý AI Bác sĩ (Tóm tắt bệnh sử & Lời dặn)
- [ ] Viết Service gửi toàn bộ bệnh sử của bệnh nhân sang AI để tóm tắt thành dạng Markdown rút gọn khi bác sĩ mở ca khám (Backend). - **(Thành viên B)**
- [ ] Xây dựng AI Service tự động sinh "Lời dặn y khoa" dựa vào mã bệnh ICD-10 của ca khám hiện tại. - **(Thành viên B)**

### MC-14: Biểu đồ thống kê và Báo cáo (Admin)
- [ ] Thiết kế Dashboard báo cáo của Admin (Frontend). - **(Thành viên C)**
- [ ] Viết API thống kê số lượt khám, số bệnh nhân duy nhất, phân bố bệnh lý theo chuyên khoa (Backend). - **(Thành viên A)**
- [ ] Vẽ biểu đồ tròn và biểu đồ cột trực quan bằng thư viện Chart.js. - **(Thành viên C)**
