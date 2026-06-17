# KẾ HOẠCH PHÂN CHIA CÔNG VIỆC NHÓM (TEAM ASSIGNMENT)

Dự án MediCore bao gồm 4 thành viên. Dưới đây là kế hoạch phân vai và chia nhỏ nhiệm vụ chi tiết theo từng Sprint để tối ưu hóa phát triển song song, giảm thiểu xung đột code (git conflict).

---

## 👥 Vai trò các thành viên (Roles)

1. **Thành viên A (Dev 1 - Backend & Database Lead)**: Chịu trách nhiệm thiết kế Database (PostgreSQL), ORM models, migrations và viết các API CRUD cơ bản.
2. **Thành viên B (Dev 2 - Backend Integration & AI Specialist)**: Chịu trách nhiệm về Logic nghiệp vụ phức tạp (Services), cổng kết nối thời gian thực (WebSocket STOMP), xuất tệp PDF và tích hợp Trợ lý AI (Gemini/OpenAI + LangChain + PgVector).
3. **Thành viên C (Dev 3 - Frontend Lead & UI Designer)**: Chịu trách nhiệm khởi tạo dự án Next.js, xây dựng Layout dùng chung, cấu hình Tailwind/Ant Design và phát triển các giao diện quản trị (Admin portal, quản lý danh mục, lịch trực, biểu đồ thống kê).
4. **Thành viên D (Dev 4 - Frontend Interaction Specialist)**: Chịu trách nhiệm phát triển các tương tác người dùng phức tạp (Cổng đặt lịch bệnh nhân, Dashboard hàng chờ real-time của bác sĩ, màn hình Chat AI, xuất PDF frontend, định tuyến Route Guards bảo vệ phân quyền).

---

## 📅 Phân chia công việc theo từng Sprint

### 🛠️ SPRINT 1: NỀN TẢNG & BẢO MẬT (FOUNDATION)

| Thành viên | Nhiệm vụ chính | Mã Backlog | Link tài liệu |
| :--- | :--- | :--- | :--- |
| **Thành viên A** (Dev 1) | - Thiết kế chi tiết sơ đồ thực thể ERD.<br>- Viết script SQL tạo bảng PostgreSQL.<br>- Khởi tạo dự án FastAPI, kết nối DB & cấu hình core. | **MC-01**, **MC-02** | [MC-01.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-01.md)<br>[MC-02.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-02.md) |
| **Thành viên B** (Dev 2) | - Viết module tự động sinh mã định danh `patient_code` & `emr_code`.<br>- Viết API Đăng ký, Đăng nhập, cấu hình JWT Token & Phân quyền, lọc chống spam SĐT. | **MC-15**, **MC-03** | [MC-15.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-15.md)<br>[MC-03.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-03.md) |
| **Thành viên C** (Dev 3) | - Khởi tạo dự án Next.js (App Router), Ant Design, Tailwind config.<br>- Thiết lập khung Layout dùng chung: `MainLayout` (sidebar linh động theo role) và `AuthLayout`. | **MC-02** | [MC-02.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-02.md) |
| **Thành viên D** (Dev 4) | - Thiết kế giao diện Đăng ký, Đăng nhập.<br>- Viết Next.js Middleware kiểm soát Route Guard (ngăn chặn bệnh nhân vào trang admin). | **MC-03** | [MC-03.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-03.md) |

---

### 📅 SPRINT 2: QUẢN TRỊ & ĐẶT LỊCH (CORE FLOW - PART 1)

| Thành viên | Nhiệm vụ chính | Mã Backlog | Link tài liệu |
| :--- | :--- | :--- | :--- |
| **Thành viên A** (Dev 1) | - Viết APIs CRUD cho Chuyên khoa, Bác sĩ.<br>- Viết APIs CRUD cho Thuốc và mã bệnh ICD-10. | **MC-04**, **MC-05** | [MC-04.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-04.md)<br>[MC-05.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-05.md) |
| **Thành viên B** (Dev 2) | - Viết logic import file dữ liệu Thuốc & ICD-10 hàng loạt.<br>- Viết API Đặt lịch khám: logic gán bác sĩ tự động (Round Robin) & logic chặn spam (tối đa 2 lịch waiting). | **MC-05**, **MC-06** | [MC-05.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-05.md)<br>[MC-06.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-06.md) |
| **Thành viên C** (Dev 3) | - Thiết kế giao diện Admin quản lý bác sĩ, chuyên khoa & gán ca trực.<br>- Thiết kế màn hình Admin quản lý Thuốc, ICD-10 & nút Import file. | **MC-04**, **MC-05** | [MC-04.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-04.md)<br>[MC-05.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-05.md) |
| **Thành viên D** (Dev 4) | - Thiết kế giao diện Bệnh nhân đặt lịch khám trực tuyến (chọn khoa, bác sĩ, ngày, chọn time slot trống). | **MC-06** | [MC-06.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-06.md) |

---

### 🩺 SPRINT 3: NGHIỆP VỤ BÁC SĨ & REAL-TIME (CORE FLOW - PART 2)

| Thành viên | Nhiệm vụ chính | Mã Backlog | Link tài liệu |
| :--- | :--- | :--- | :--- |
| **Thành viên A** (Dev 1) | - Viết API lưu trữ Bệnh án điện tử (EMR) từ bác sĩ khám.<br>- Thiết lập cơ chế chặn sửa đổi bệnh án sau khi đã hoàn thành khám. | **MC-09** | [MC-09.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-09.md) |
| **Thành viên B** (Dev 2) | - Thiết lập Gateway WebSocket STOMP Server trên FastAPI.<br>- Viết logic đẩy tin gọi số thứ tự về phía người dùng khi bác sĩ click nút khám. | **MC-07** | [MC-07.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-07.md) |
| **Thành viên C** (Dev 3) | - Thiết kế giao diện khám bệnh của Bác sĩ: ô nhập triệu chứng, chọn mã bệnh ICD-10 (hỗ trợ Debounce Search để tối ưu gọi API). | **MC-09** | [MC-09.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-09.md) |
| **Thành viên D** (Dev 4) | - Thiết lập WebSocket Client kết nối Next.js với Backend.<br>- Thiết kế giao diện Dashboard hàng chờ gọi khám thời gian thực của Bác sĩ. | **MC-07**, **MC-08** | [MC-07.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-07.md)<br>[MC-08.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-08.md) |

---

### 🤖 SPRINT 4: AI & HOÀN THIỆN (POLISHING)

| Thành viên | Nhiệm vụ chính | Mã Backlog | Link tài liệu |
| :--- | :--- | :--- | :--- |
| **Thành viên A** (Dev 1) | - Viết API tổng hợp báo cáo thống kê phòng khám (tổng ca khám, tổng số bệnh nhân duy nhất, biểu đồ các khoa). | **MC-14** | [MC-14.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-14.md) |
| **Thành viên B** (Dev 2) | - Viết hàm tự sinh PDF đơn thuốc từ kết quả khám.<br>- Xây dựng AI Service 1: RAG gợi ý khoa khám (MC-12).<br>- Xây dựng AI Service 2: Tóm tắt bệnh sử & sinh lời dặn tự động (MC-13). | **MC-10**, **MC-12**, **MC-13** | [MC-10.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-10.md)<br>[MC-12.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-12.md)<br>[MC-13.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-13.md) |
| **Thành viên C** (Dev 3) | - Thiết kế giao diện báo cáo thống kê Admin, vẽ biểu đồ tròn/biểu đồ cột sử dụng thư viện Chart.js. | **MC-14** | [MC-14.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-14.md) |
| **Thành viên D** (Dev 4) | - Thiết kế giao diện chat Trợ lý AI Bệnh nhân.<br>- Thiết kế màn hình xem bệnh sử (Timeline) bệnh nhân & in đơn thuốc PDF.<br>- Hiển thị nội dung AI tóm tắt trên màn hình khám của Bác sĩ. | **MC-10**, **MC-11**, **MC-12**, **MC-13** | [MC-10.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-10.md)<br>[MC-11.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-11.md)<br>[MC-12.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-12.md)<br>[MC-13.md](file:///Users/doando/Documents/rikkei/docs/backlogs/backlog-list/MC-13.md) |
