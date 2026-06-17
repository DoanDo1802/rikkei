# Hướng dẫn sử dụng Supabase Database

## 📋 Cấu trúc thư mục

```
backend/
├── .env                    # Credentials Supabase (không commit)
├── requirements.txt        # Dependencies
├── supabase_db.py         # Module kết nối database
├── query_data.py          # Script test kết nối
├── test_queries.py        # Test queries cho tất cả các bảng
├── examples.py            # Ví dụ sử dụng
└── DATABASE.md            # Tài liệu này
```

## 🚀 Cài đặt

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Kiểm tra kết nối
```bash
python query_data.py
```

### 3. Test tất cả các bảng
```bash
python test_queries.py
```

## 📊 Sử dụng trong code

### Import module
```python
from supabase_db import db
```

## 📁 Các bảng chính

| Bảng | Mô tả | Task liên quan |
|------|-------|----------------|
| `users` | Tài khoản người dùng (liên kết Supabase Auth) | Tất cả |
| `specialties` | Danh sách chuyên khoa | MC-03, MC-04 |
| `diseases` | Danh mục bệnh (mã ICD-10) | MC-06 |
| `medicines` | Danh mục thuốc | MC-07 |
| `patients` | Hồ sơ bệnh nhân | MC-01, MC-02 |
| `doctors` | Hồ sơ bác sĩ | MC-03 |
| `doctor_schedules` | Lịch trực bác sĩ | MC-04 |
| `appointments` | Hẹn khám | MC-05, MC-08, MC-14 |
| `medical_records` | Hồ sơ bệnh án điện tử (EMR) | MC-06 |
| `prescriptions` | Đơn thuốc | MC-07 |
| `prescription_details` | Chi tiết đơn thuốc | MC-07 |
| `ai_consultation_logs` | Nhật ký tư vấn AI | MC-12 |

## 🔍 Các truy vấn thường dùng

### 1️⃣ USERS - Quản lý tài khoản
```python
# Lấy tất cả người dùng
users = db.select('users', limit=20)

# Lấy tất cả admin
admins = db.select_where('users', 'role', 'ADMIN')

# Lấy tất cả bác sĩ
doctors_users = db.select_where('users', 'role', 'DOCTOR')

# Lấy tất cả bệnh nhân
patient_users = db.select_where('users', 'role', 'PATIENT')
```

### 2️⃣ SPECIALTIES - Chuyên khoa
```python
# Lấy tất cả chuyên khoa
specialties = db.select('specialties')

# Tìm chuyên khoa theo ID
specialty = db.select_where('specialties', 'id', 1)
```

### 3️⃣ DISEASES - Danh mục bệnh (ICD-10)
```python
# Lấy danh mục bệnh
diseases = db.select('diseases', limit=20)

# Tìm bệnh theo mã ICD-10
disease = db.select_where('diseases', 'icd10_code', 'J45.9')
```

### 4️⃣ MEDICINES - Thuốc
```python
# Lấy danh sách thuốc
medicines = db.select('medicines', limit=20)

# Tìm thuốc theo ID
medicine = db.select_where('medicines', 'id', 1)
```

### 5️⃣ PATIENTS - Bệnh nhân (MC-01, MC-02)
```python
# Lấy tất cả bệnh nhân
patients = db.select('patients', limit=10)

# Tìm bệnh nhân theo mã
patient = db.select_where('patients', 'patient_code', 'P001')

# Lấy bệnh nhân theo số điện thoại
patient = db.select_where('patients', 'phone', '0912345678')

# Thêm bệnh nhân mới
new_patient = db.insert('patients', {
    'user_id': 'uuid-from-auth',
    'patient_code': 'P001',
    'full_name': 'Nguyễn Văn A',
    'dob': '1990-01-15',
    'gender': 'MALE',
    'phone': '0912345678',
    'address': '123 Đường ABC, TP HCM'
})

# Cập nhật bệnh nhân
db.update('patients', {
    'full_name': 'Nguyễn Văn B',
    'phone': '0987654321'
}, 'patient_code', 'P001')
```

### 6️⃣ DOCTORS - Bác sĩ (MC-03)
```python
# Lấy tất cả bác sĩ
doctors = db.select('doctors', limit=10)

# Tìm bác sĩ theo mã
doctor = db.select_where('doctors', 'doctor_code', 'D001')

# Thêm bác sĩ mới
new_doctor = db.insert('doctors', {
    'user_id': 'uuid-from-auth',
    'specialty_id': 1,
    'doctor_code': 'D001',
    'doctor_name': 'Trần Văn X',
    'phone': '0911111111',
    'degree': 'MD, Cardiologist',
    'experience_years': 10
})

# Cập nhật bác sĩ
db.update('doctors', {
    'experience_years': 11
}, 'doctor_code', 'D001')
```

### 7️⃣ DOCTOR_SCHEDULES - Lịch trực (MC-04)
```python
# Lấy lịch trực của bác sĩ
schedules = db.select('doctor_schedules', limit=20)

# Lấy các slot chưa được đặt (còn trống)
available_slots = db.select_where('doctor_schedules', 'is_booked', False)

# Lấy các slot đã được đặt
booked_slots = db.select_where('doctor_schedules', 'is_booked', True)

# Thêm lịch trực
new_schedule = db.insert('doctor_schedules', {
    'doctor_id': 1,
    'work_date': '2026-06-20',
    'time_slot': '08:00-09:00',
    'is_booked': False
})

# Đánh dấu slot đã được đặt
db.update('doctor_schedules', {
    'is_booked': True
}, 'id', 1)
```

### 8️⃣ APPOINTMENTS - Hẹn khám (MC-05, MC-08, MC-14)
```python
# Lấy tất cả hẹn khám
appointments = db.select('appointments', limit=20)

# Lấy hẹn khám chờ xử lý - MC-08
waiting = db.select_where('appointments', 'status', 'WAITING')

# Lấy hẹn khám đang khám
in_progress = db.select_where('appointments', 'status', 'IN_PROGRESS')

# Lấy hẹn khám hoàn thành
done = db.select_where('appointments', 'status', 'DONE')

# Lấy hẹn khám hủy
cancelled = db.select_where('appointments', 'status', 'CANCELLED')

# Thêm hẹn khám mới - MC-05
new_appointment = db.insert('appointments', {
    'patient_id': 'P001',
    'doctor_id': 1,
    'appointment_date': '2026-06-20',
    'time_slot': '08:00-09:00',
    'symptoms_initial': 'Đau đầu, sốt cao',
    'status': 'WAITING'
})

# Cập nhật trạng thái hẹn khám - MC-08
db.update('appointments', {
    'status': 'DONE'
}, 'id', 1)

# Hủy hẹn khám
db.update('appointments', {
    'status': 'CANCELLED'
}, 'id', 1)
```

### 9️⃣ MEDICAL_RECORDS - Bệnh án (MC-06)
```python
# Lấy tất cả bệnh án
medical_records = db.select('medical_records', limit=10)

# Tìm bệnh án theo mã EMR
emr = db.select_where('medical_records', 'emr_code', 'EMR001')

# Lấy bệnh án của bệnh nhân
patient_records = db.select_where('medical_records', 'patient_id', 'P001')

# Tạo bệnh án mới
new_record = db.insert('medical_records', {
    'emr_code': 'EMR001',
    'appointment_id': 1,
    'patient_id': 'P001',
    'doctor_id': 1,
    'diagnosis_icd10': 'J45.9',
    'clinical_note': 'Bệnh nhân có triệu chứng súc khí...',
    'history_summary': 'Tiền sử dị ứng...',
    'care_advice': 'Kiêng dầu mỡ, nghỉ ngơi đủ'
})

# Cập nhật bệnh án
db.update('medical_records', {
    'diagnosis_icd10': 'J45.0',
    'clinical_note': 'Cập nhật chẩn đoán'
}, 'emr_code', 'EMR001')
```

### 🔟 PRESCRIPTIONS - Đơn thuốc (MC-07)
```python
# Lấy tất cả đơn thuốc
prescriptions = db.select('prescriptions', limit=10)

# Lấy đơn thuốc của bệnh án
record_prescriptions = db.select_where('prescriptions', 'medical_record_id', 1)

# Tạo đơn thuốc mới
new_prescription = db.insert('prescriptions', {
    'medical_record_id': 1,
    'pdf_url': 'https://...pdf-url'
})
```

### 1️⃣1️⃣ PRESCRIPTION_DETAILS - Chi tiết đơn thuốc (MC-07)
```python
# Lấy chi tiết đơn thuốc
prescription_details = db.select('prescription_details', limit=20)

# Lấy chi tiết của đơn
details = db.select_where('prescription_details', 'prescription_id', 1)

# Thêm chi tiết đơn thuốc
new_detail = db.insert('prescription_details', {
    'prescription_id': 1,
    'medicine_id': 1,
    'quantity': 2,
    'dosage_instruction': 'Uống 1 viên 2 lần/ngày, sau ăn'
})
```

### 1️⃣2️⃣ AI_CONSULTATION_LOGS - Nhật ký AI (MC-12)
```python
# Lấy nhật ký AI
ai_logs = db.select('ai_consultation_logs', limit=20)

# Lấy nhật ký của bệnh nhân
patient_logs = db.select_where('ai_consultation_logs', 'patient_id', 1)

# Thêm nhật ký AI
new_log = db.insert('ai_consultation_logs', {
    'patient_id': 1,
    'symptom_input': 'Đau đầu, sốt cao, chóng mặt',
    'suggested_specialty_id': 2,
    'ai_reasoning': 'Based on symptoms analysis, likely neurological issue'
})
```

## 💡 Ví dụ tích hợp - Tạo hẹn khám

```python
from supabase_db import db

def create_appointment_with_schedule():
    """Ví dụ: Tạo hẹn khám và cập nhật lịch trực"""
    
    # 1. Tìm slot trống
    available = db.select_where('doctor_schedules', 'is_booked', False)
    if not available:
        print("No available slots")
        return
    
    slot = available[0]
    
    # 2. Tạo hẹn khám
    appointment = db.insert('appointments', {
        'patient_id': 'P001',
        'doctor_id': slot['doctor_id'],
        'appointment_date': slot['work_date'],
        'time_slot': slot['time_slot'],
        'symptoms_initial': 'Đau đầu',
        'status': 'WAITING'
    })
    
    # 3. Đánh dấu slot đã được đặt
    db.update('doctor_schedules', {
        'is_booked': True
    }, 'id', slot['id'])
    
    print(f"✓ Appointment created: {appointment}")
    return appointment

# Chạy ví dụ
# create_appointment_with_schedule()
```

## 🔍 Debugging

**Kiểm tra .env file**
```bash
cat .env
```

**Test kết nối trực tiếp**
```bash
python -c "from supabase_db import db; print(db.select('patients', limit=1))"
```

**Xem lỗi chi tiết**
```python
try:
    data = db.select('table_name')
except Exception as e:
    print(f"Error: {e}")
```

## ⚠️ Lưu ý quan trọng

1. **Không commit .env file** - Chỉ chia sẻ với team thông qua kênh an toàn
2. **Luôn sử dụng load_dotenv()** - Để tải credentials từ .env
3. **Xử lý lỗi** - Kiểm tra null/exception khi truy vấn
4. **Indexes** - Hệ thống đã tạo indexes để tối ưu tìm kiếm theo:
   - `patient_code` (bệnh nhân)
   - `doctor_code` (bác sĩ)
   - `appointment_date` (ngày khám)
   - `status` (trạng thái hẹn khám)
   - `emr_code` (mã bệnh án)

## 📞 Support

Nếu gặp lỗi, hãy kiểm tra:
1. Credentials Supabase có đúng không?
2. Tên bảng có chính xác không?
3. Internet connection có ổn định không?
