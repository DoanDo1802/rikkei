# Hướng dẫn Supabase Database Setup

Tài liệu hướng dẫn sử dụng Supabase database cho hệ thống quản lý bệnh viện.

## 📦 Các thành phần mới

Các file dưới đây được tạo để quản lý kết nối với Supabase:

| File | Mô tả |
|------|-------|
| `supabase_db.py` | **Module core** - Kết nối database & các phương thức CRUD |
| `query_data.py` | Script test kết nối Supabase |
| `test_queries.py` | Test tất cả các bảng trong database |
| `examples.py` | Ví dụ sử dụng module |
| `api_endpoints.py` | API REST endpoints dùng Flask |
| `DATABASE.md` | Tài liệu chi tiết về cấu trúc database |
| `SUPABASE_SETUP.md` | Tài liệu này |

## 🚀 Cài đặt nhanh

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Kiểm tra kết nối
```bash
python query_data.py
```

Kết quả thành công sẽ hiển thị:
```
============================================================
Supabase Database Connection Test
============================================================
✓ Supabase client initialized successfully
URL: https://pabogdocgaqzxfehrbhc.supabase.co
```

### 3. Test tất cả các bảng (tuỳ chọn)
```bash
python test_queries.py
```

## 💾 Database Schema (13 bảng)

```
📊 Database Schema
├── 👤 users                    - Tài khoản người dùng (Supabase Auth)
├── 🏥 specialties              - Chuyên khoa (MC-03, MC-04)
├── 🦠 diseases                 - Danh mục bệnh ICD-10
├── 💊 medicines                - Danh mục thuốc
├── 😷 patients                 - Bệnh nhân (MC-01, MC-02)
├── 👨‍⚕️ doctors                 - Bác sĩ (MC-03)
├── 📅 doctor_schedules         - Lịch trực (MC-04)
├── 📋 appointments             - Hẹn khám (MC-05, MC-08, MC-14)
├── 🗂️ medical_records          - Bệnh án EMR (MC-06)
├── 📝 prescriptions            - Đơn thuốc (MC-07)
├── 💾 prescription_details     - Chi tiết đơn (MC-07)
└── 🤖 ai_consultation_logs     - Nhật ký AI (MC-12)
```

## 🔌 Sử dụng Module supabase_db.py

### Import
```python
from supabase_db import db
```

### Các phương thức có sẵn

```python
# SELECT
data = db.select(table, columns="*", limit=100)
data = db.select_where(table, column, value, columns="*")

# INSERT
result = db.insert(table, data_dict)
results = db.insert_many(table, list_of_dicts)

# UPDATE
updated = db.update(table, data_dict, filter_column, filter_value)

# DELETE
db.delete(table, filter_column, filter_value)
```

### Ví dụ

```python
from supabase_db import db

# Lấy 10 bệnh nhân
patients = db.select('patients', limit=10)

# Tìm bệnh nhân theo mã
patient = db.select_where('patients', 'patient_code', 'P001')

# Thêm bệnh nhân mới
new_patient = db.insert('patients', {
    'patient_code': 'P001',
    'full_name': 'Nguyễn Văn A',
    'phone': '0912345678'
})

# Cập nhật
db.update('patients', {
    'full_name': 'Nguyễn Văn B'
}, 'patient_code', 'P001')

# Xóa
db.delete('patients', 'patient_code', 'P001')
```

## 🔥 Các truy vấn thường dùng

### 1. Quản lý bệnh nhân (MC-01, MC-02)
```python
# Lấy tất cả bệnh nhân
patients = db.select('patients')

# Tìm bệnh nhân
patient = db.select_where('patients', 'patient_code', 'P001')
patient = db.select_where('patients', 'phone', '0912345678')

# Thêm bệnh nhân
db.insert('patients', {
    'patient_code': 'P001',
    'full_name': 'Nguyễn Văn A',
    'dob': '1990-01-15',
    'gender': 'MALE',
    'phone': '0912345678',
    'address': '123 Đường ABC, TP HCM'
})
```

### 2. Quản lý bác sĩ (MC-03)
```python
# Lấy danh sách bác sĩ
doctors = db.select('doctors')

# Lấy bác sĩ theo chuyên khoa
specialists = db.select_where('doctors', 'specialty_id', 2)
```

### 3. Lịch trực bác sĩ (MC-04)
```python
# Lấy slot còn trống
available = db.select_where('doctor_schedules', 'is_booked', False)

# Đánh dấu slot đã được đặt
db.update('doctor_schedules', {
    'is_booked': True
}, 'id', slot_id)
```

### 4. Hẹn khám (MC-05, MC-08, MC-14)
```python
# Lấy hẹn khám chờ xử lý
waiting = db.select_where('appointments', 'status', 'WAITING')

# Lấy hẹn khám hoàn thành
done = db.select_where('appointments', 'status', 'DONE')

# Cập nhật trạng thái hẹn khám
db.update('appointments', {
    'status': 'DONE'
}, 'id', appointment_id)

# Tạo hẹn khám mới
db.insert('appointments', {
    'patient_id': 'P001',
    'doctor_id': 1,
    'appointment_date': '2026-06-20',
    'time_slot': '08:00-09:00',
    'status': 'WAITING'
})
```

### 5. Bệnh án (MC-06)
```python
# Lấy bệnh án
records = db.select('medical_records')

# Lấy bệnh án của bệnh nhân
patient_records = db.select_where('medical_records', 'patient_id', 'P001')

# Tạo bệnh án
db.insert('medical_records', {
    'emr_code': 'EMR001',
    'appointment_id': 1,
    'patient_id': 'P001',
    'doctor_id': 1,
    'diagnosis_icd10': 'J45.9',
    'clinical_note': 'Bệnh nhân khỏe mạnh'
})
```

### 6. Đơn thuốc (MC-07)
```python
# Lấy đơn thuốc
prescriptions = db.select('prescriptions')

# Lấy chi tiết đơn
details = db.select_where('prescription_details', 'prescription_id', 1)

# Tạo đơn thuốc
db.insert('prescriptions', {
    'medical_record_id': 1,
    'pdf_url': 'https://...'
})

# Thêm chi tiết đơn
db.insert('prescription_details', {
    'prescription_id': 1,
    'medicine_id': 1,
    'quantity': 2,
    'dosage_instruction': 'Uống 1 viên 2 lần/ngày'
})
```

### 7. Nhật ký AI (MC-12)
```python
# Lấy nhật ký AI
logs = db.select('ai_consultation_logs')

# Tạo nhật ký mới
db.insert('ai_consultation_logs', {
    'patient_id': 1,
    'symptom_input': 'Đau đầu, sốt cao',
    'suggested_specialty_id': 2,
    'ai_reasoning': 'Based on symptoms...'
})
```

## 🌐 API Endpoints (Flask)

Nếu muốn chạy API REST:

```bash
pip install flask flask-cors
python api_endpoints.py
```

API sẽ chạy tại `http://localhost:5000`

### Available endpoints
```
GET  /api/patients
POST /api/patients
GET  /api/doctors
GET  /api/appointments
POST /api/appointments
GET  /api/appointments/waiting
GET  /api/medical-records
POST /api/medical-records
GET  /api/prescriptions
GET  /api/ai-logs
GET  /api/statistics/appointments
```

## 🛠️ Tích hợp vào FastAPI

Nếu đang dùng FastAPI:

```python
from fastapi import APIRouter
from supabase_db import db

router = APIRouter()

@router.get("/patients")
async def get_patients():
    patients = db.select('patients', limit=10)
    return {
        'success': True,
        'data': patients
    }

@router.post("/patients")
async def create_patient(data: dict):
    patient = db.insert('patients', data)
    return {
        'success': True,
        'data': patient[0] if patient else None
    }
```

## 📊 Ví dụ Workflow hoàn chỉnh

### Workflow: Tạo hẹn khám và bệnh án

```python
from supabase_db import db

def complete_appointment_flow(patient_code, doctor_id):
    """
    Quy trình hoàn chỉnh:
    1. Tìm slot trống
    2. Tạo hẹn khám
    3. Cập nhật slot
    4. Tạo bệnh án
    5. Thêm đơn thuốc
    """
    
    # 1. Tìm slot trống
    available = db.select_where('doctor_schedules', 'doctor_id', doctor_id)
    slots = [s for s in available if not s['is_booked']]
    
    if not slots:
        return {'error': 'No available slots'}
    
    slot = slots[0]
    
    # 2. Tạo hẹn khám
    appointment = db.insert('appointments', {
        'patient_id': patient_code,
        'doctor_id': doctor_id,
        'appointment_date': slot['work_date'],
        'time_slot': slot['time_slot'],
        'status': 'WAITING'
    })
    
    appointment_id = appointment[0]['id'] if appointment else None
    
    # 3. Đánh dấu slot
    db.update('doctor_schedules', {
        'is_booked': True
    }, 'id', slot['id'])
    
    # 4. Tạo bệnh án
    record = db.insert('medical_records', {
        'emr_code': f"EMR{appointment_id}",
        'appointment_id': appointment_id,
        'patient_id': patient_code,
        'doctor_id': doctor_id,
        'diagnosis_icd10': 'J45.9',
        'clinical_note': 'Khám sức khỏe định kỳ'
    })
    
    # 5. Thêm đơn thuốc
    if record:
        prescription = db.insert('prescriptions', {
            'medical_record_id': record[0]['id'],
            'pdf_url': 'pending'
        })
    
    # 6. Cập nhật hẹn khám thành DONE
    db.update('appointments', {
        'status': 'DONE'
    }, 'id', appointment_id)
    
    return {
        'success': True,
        'appointment': appointment[0] if appointment else None,
        'record': record[0] if record else None
    }

# Sử dụng
result = complete_appointment_flow('P001', 1)
print(result)
```

## 🐛 Debugging & Troubleshooting

### Kiểm tra kết nối
```bash
python -c "from supabase_db import db; print(db.select('patients', limit=1))"
```

### Xem lỗi chi tiết
```python
try:
    data = db.select('patients')
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

### Kiểm tra .env
```bash
cat .env
```

### Vấn đề thường gặp

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-----------|----------|
| `supabase_url is required` | .env không load | Kiểm tra path .env |
| `PGRST205` | Bảng không tồn tại | Kiểm tra tên bảng |
| Connection timeout | Internet không ổn | Kiểm tra kết nối mạng |
| `Role` errors | Permissions bị từ chối | Kiểm tra RLS trên Supabase |

## 🔐 Bảo mật

1. **Không commit .env** - Thêm vào `.gitignore`
2. **Protect credentials** - Không share key công khai
3. **Enable RLS** - Bật Row-Level Security trên Supabase
4. **Validate input** - Luôn kiểm tra dữ liệu từ client

## 📚 Tài liệu tham khảo

- [DATABASE.md](DATABASE.md) - Tài liệu chi tiết database
- [test_queries.py](test_queries.py) - Xem ví dụ truy vấn
- [api_endpoints.py](api_endpoints.py) - Xem API endpoints
- [Supabase Docs](https://supabase.com/docs)
- [Python Supabase Client](https://github.com/supabase-community/supabase-py)

## 💡 Tips

1. **Test từng bước** - Không nên tạo logic quá phức tạp một lần
2. **Sử dụng transactions** - Đảm bảo dữ liệu nhất quán
3. **Thêm logging** - Giúp debug dễ hơn
4. **Validate dữ liệu** - Trước khi insert/update
5. **Handle errors** - Luôn dùng try-except

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra [DATABASE.md](DATABASE.md) để xem cấu trúc database
2. Chạy [test_queries.py](test_queries.py) để kiểm tra kết nối
3. Xem logs của Flask hoặc Python
4. Kiểm tra Supabase Dashboard

---

**Cập nhật lần cuối**: 2026-06-17  
**Phiên bản**: 1.0  
**Status**: ✅ Sẵn sàng sản xuất
