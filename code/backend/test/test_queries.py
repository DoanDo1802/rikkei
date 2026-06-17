"""
Test queries for Medical Management System
Truy vấn dữ liệu từ các bảng trong hệ thống quản lý bệnh viện
"""

from supabase_db import db
import json
from datetime import datetime

def print_header(title):
    """In tiêu đề"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_table(data, limit=5):
    if data is None: # Nếu db.select trả về None khi lỗi
        print("❌ Lỗi kết nối hoặc bảng không tồn tại")
        return
    if len(data) == 0:
        print("⚠️ Bảng tồn tại nhưng hiện đang TRỐNG (0 bản ghi)")
        return
    
    print(f"✓ Tìm thấy {len(data)} bản ghi:")
    for idx, record in enumerate(data[:limit], 1):
        print(f"\nBản ghi {idx}:")
        for key, value in record.items():
            print(f"  {key}: {value}")

# ============================================================
# USERS (Tài khoản người dùng - liên kết Supabase Auth)
# ============================================================
def test_users():
    """Truy vấn bảng người dùng"""
    print_header("Bảng USERS - Tài khoản người dùng")
    data = db.select('users', limit=10)
    print_table(data)
    return data

# ============================================================
# CHUYÊN KHOA (SPECIALTIES)
# ============================================================
def test_specialties():
    """Truy vấn bảng chuyên khoa"""
    print_header("Bảng SPECIALTIES - Danh sách chuyên khoa")
    data = db.select('specialties', limit=10)
    print_table(data)
    return data

# ============================================================
# BỆNH (DISEASES) - Danh mục mã ICD-10
# ============================================================
def test_diseases():
    """Truy vấn bảng bệnh - Mã ICD-10"""
    print_header("Bảng DISEASES - Danh mục bệnh (ICD-10)")
    data = db.select('diseases', limit=10)
    print_table(data)
    return data

# ============================================================
# THUỐC (MEDICINES)
# ============================================================
def test_medicines():
    """Truy vấn bảng thuốc"""
    print_header("Bảng MEDICINES - Danh mục thuốc")
    data = db.select('medicines', limit=10)
    print_table(data)
    return data

# ============================================================
# BỆNH NHÂN (PATIENTS)
# ============================================================
def test_patients():
    """Truy vấn bảng bệnh nhân"""
    print_header("Bảng PATIENTS - Thông tin bệnh nhân")
    data = db.select('patients', limit=10)
    print_table(data)
    return data

# ============================================================
# BÁC SĨ (DOCTORS)
# ============================================================
def test_doctors():
    """Truy vấn bảng bác sĩ"""
    print_header("Bảng DOCTORS - Thông tin bác sĩ")
    data = db.select('doctors', limit=10)
    print_table(data)
    
    # Phân tích số bác sĩ theo chuyên khoa
    if data:
        print("\n--- Thống kê bác sĩ theo chuyên khoa ---")
        specialties = {}
        for doctor in data:
            spec_id = doctor.get('specialty_id')
            if spec_id:
                specialties[spec_id] = specialties.get(spec_id, 0) + 1
        for spec_id, count in sorted(specialties.items(), key=lambda x: x[1], reverse=True):
            print(f"  Chuyên khoa ID {spec_id}: {count} bác sĩ")
    
    return data

# ============================================================
# LỊCH TRỰC BÁC SĨ (DOCTOR_SCHEDULES) - MC-04
# ============================================================
def test_doctor_schedules():
    """Truy vấn bảng lịch trực bác sĩ - MC-04"""
    print_header("Bảng DOCTOR_SCHEDULES - Lịch trực bác sĩ (MC-04)")
    data = db.select('doctor_schedules', limit=10)
    print_table(data)
    
    # Thống kê slot trống
    available = db.select_where('doctor_schedules', 'is_booked', False)
    booked = db.select_where('doctor_schedules', 'is_booked', True)
    
    print("\n--- Thống kê lịch trực ---")
    if available:
        print(f"  ✓ Slot trống (is_booked=false): {len(available)} slot")
    if booked:
        print(f"  ✓ Slot đã đặt (is_booked=true): {len(booked)} slot")
    
    return data

# ============================================================
# HẸN KHÁM (APPOINTMENTS) - MC-05, MC-08, MC-14
# ============================================================
def test_appointments():
    """Truy vấn bảng hẹn khám"""
    print_header("Bảng APPOINTMENTS - Danh sách hẹn khám (MC-05, MC-08, MC-14)")
    data = db.select('appointments', limit=10)
    print_table(data)
    
    # Thống kê theo trạng thái - MC-08, MC-14
    print("\n--- Thống kê theo trạng thái hẹn khám (MC-08) ---")
    waiting = db.select_where('appointments', 'status', 'WAITING')
    in_progress = db.select_where('appointments', 'status', 'IN_PROGRESS')
    done = db.select_where('appointments', 'status', 'DONE')
    cancelled = db.select_where('appointments', 'status', 'CANCELLED')
    
    if waiting:
        print(f"  ⏳ Chờ khám (WAITING): {len(waiting)} ca")
    if in_progress:
        print(f"  🏥 Đang khám (IN_PROGRESS): {len(in_progress)} ca")
    if done:
        print(f"  ✓ Hoàn thành (DONE): {len(done)} ca")
    if cancelled:
        print(f"  ✗ Hủy (CANCELLED): {len(cancelled)} ca")
    
    return data

# ============================================================
# BỆNH ÁN (MEDICAL_RECORDS) - MC-06
# ============================================================
def test_medical_records():
    """Truy vấn bảng bệnh án - MC-06"""
    print_header("Bảng MEDICAL_RECORDS - Hồ sơ bệnh án điện tử (MC-06)")
    data = db.select('medical_records', limit=10)
    print_table(data)
    
    # Phân tích các chẩn đoán
    if data:
        print("\n--- Thống kê chẩn đoán (ICD-10) ---")
        diagnoses = {}
        for record in data:
            icd10 = record.get('diagnosis_icd10')
            if icd10:
                diagnoses[icd10] = diagnoses.get(icd10, 0) + 1
        for icd10, count in sorted(diagnoses.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {icd10}: {count} ca")
    
    return data

# ============================================================
# ĐƠN THUỐC (PRESCRIPTIONS)
# ============================================================
def test_prescriptions():
    """Truy vấn bảng đơn thuốc"""
    print_header("Bảng PRESCRIPTIONS - Đơn thuốc")
    data = db.select('prescriptions', limit=10)
    print_table(data)
    return data

# ============================================================
# CHI TIẾT ĐƠN THUỐC (PRESCRIPTION_DETAILS)
# ============================================================
def test_prescription_details():
    """Truy vấn bảng chi tiết đơn thuốc"""
    print_header("Bảng PRESCRIPTION_DETAILS - Chi tiết đơn thuốc")
    data = db.select('prescription_details', limit=10)
    print_table(data)
    
    # Thống kê thuốc được kê đơn
    if data:
        print("\n--- Thuốc được kê đơn nhiều nhất ---")
        medicines = {}
        for detail in data:
            med_id = detail.get('medicine_id')
            if med_id:
                medicines[med_id] = medicines.get(med_id, 0) + 1
        for med_id, count in sorted(medicines.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  Thuốc ID {med_id}: {count} lần kê đơn")
    
    return data

# ============================================================
# NHẬT KÝ AI (AI_CONSULTATION_LOGS) - MC-12
# ============================================================
def test_ai_logs():
    """Truy vấn bảng nhật ký AI - MC-12"""
    print_header("Bảng AI_CONSULTATION_LOGS - Nhật ký tư vấn AI (MC-12)")
    data = db.select('ai_consultation_logs', limit=10)
    print_table(data)
    
    # Phân tích các chuyên khoa được gợi ý
    if data:
        print("\n--- Thống kê chuyên khoa được gợi ý (MC-12) ---")
        specialties = {}
        for log in data:
            spec_id = log.get('suggested_specialty_id')
            if spec_id:
                specialties[spec_id] = specialties.get(spec_id, 0) + 1
        
        for spec_id, count in sorted(specialties.items(), key=lambda x: x[1], reverse=True):
            print(f"  Chuyên khoa ID {spec_id}: {count} lần gợi ý")
    
    return data

# ============================================================
# TRUY VẤN TỰ CHỈNH
# ============================================================
def custom_query(table_name: str, column: str = None, value = None, limit: int = 10):
    """Truy vấn tuỳ chỉnh"""
    print_header(f"Truy vấn tùy chỉnh: {table_name}")
    
    if column and value:
        print(f"Tìm kiếm: {column} = {value}")
        data = db.select_where(table_name, column, value)
    else:
        data = db.select(table_name, limit=limit)
    
    print_table(data, limit=limit)
    return data

# ============================================================
# MAIN
# ============================================================
def main():
    print("\n" + "=" * 60)
    print("  HỆ THỐNG QUẢN LÝ BỆNH VIỆN - TEST QUERIES")
    print("=" * 60)
    
    # Test tất cả các bảng
    test_users()
    test_specialties()
    test_diseases()
    test_medicines()
    test_patients()
    test_doctors()
    test_doctor_schedules()
    test_appointments()
    test_medical_records()
    test_prescriptions()
    test_prescription_details()
    test_ai_logs()
    
    print("\n" + "=" * 60)
    print("  ✓ Test hoàn thành!")
    print("=" * 60)
    print("\nCách sử dụng hàm custom_query():")
    print("  custom_query('doctors', limit=20)")
    print("  custom_query('appointments', 'status', 'WAITING')")
    print("  custom_query('doctor_schedules', 'is_booked', False)")

if __name__ == "__main__":
    main()
    
    # Ví dụ sử dụng custom_query
    # custom_query('appointments', 'status', 'WAITING')
    # custom_query('doctor_schedules', 'is_booked', False)
