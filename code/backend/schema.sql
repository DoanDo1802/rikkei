-- ==========================================
-- MEDICAL MANAGEMENT SYSTEM DATABASE SCHEMA
-- ==========================================

-- 1. USERS (Liên kết chặt chẽ với Supabase Auth)
-- ==========================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('ADMIN', 'DOCTOR', 'PATIENT')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 2. SPECIALTIES (Chuyên khoa)
-- ==========================================
CREATE TABLE IF NOT EXISTS specialties (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    specialty_name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 3. DISEASES (Danh mục mã bệnh ICD-10)
-- ==========================================
CREATE TABLE IF NOT EXISTS diseases (
    icd10_code VARCHAR(10) PRIMARY KEY,
    disease_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 4. MEDICINES (Danh mục thuốc)
-- ==========================================
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    medicine_name VARCHAR(100) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 5. PATIENTS (Hồ sơ bệnh nhân)
-- ==========================================
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    patient_code VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    dob DATE,
    gender TEXT CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
    phone VARCHAR(20) UNIQUE,
    address TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 6. DOCTORS (Hồ sơ bác sĩ)
-- ==========================================
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    specialty_id INTEGER REFERENCES specialties(id),
    doctor_code VARCHAR(20) NOT NULL UNIQUE,
    doctor_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    degree VARCHAR(255),
    experience_years INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 7. DOCTOR_SCHEDULES (Lịch trực bác sĩ)
-- ==========================================
CREATE TABLE IF NOT EXISTS doctor_schedules (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    work_date DATE NOT NULL,
    time_slot VARCHAR(50) NOT NULL,
    is_booked BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 8. APPOINTMENTS (Lịch hẹn khám)
-- ==========================================
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id VARCHAR(20) REFERENCES patients(patient_code),
    doctor_id INTEGER REFERENCES doctors(id),
    appointment_date DATE NOT NULL,
    time_slot VARCHAR(50) NOT NULL,
    symptoms_initial TEXT,
    status TEXT NOT NULL DEFAULT 'WAITING' 
        CHECK (status IN ('WAITING', 'IN_PROGRESS', 'DONE', 'CANCELLED')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 9. MEDICAL RECORDS (Hồ sơ bệnh án điện tử)
-- ==========================================
CREATE TABLE IF NOT EXISTS medical_records (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    emr_code VARCHAR(30) NOT NULL UNIQUE,
    appointment_id INTEGER REFERENCES appointments(id),
    patient_id VARCHAR(20) REFERENCES patients(patient_code),
    doctor_id INTEGER REFERENCES doctors(id),
    diagnosis_icd10 VARCHAR(10) REFERENCES diseases(icd10_code),
    clinical_note TEXT,
    history_summary TEXT,
    care_advice TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 10. PRESCRIPTIONS (Đơn thuốc)
-- ==========================================
CREATE TABLE IF NOT EXISTS prescriptions (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    medical_record_id INTEGER REFERENCES medical_records(id) ON DELETE CASCADE,
    pdf_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 11. PRESCRIPTION DETAILS (Chi tiết đơn thuốc)
-- ==========================================
CREATE TABLE IF NOT EXISTS prescription_details (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    prescription_id INTEGER REFERENCES prescriptions(id) ON DELETE CASCADE,
    medicine_id INTEGER REFERENCES medicines(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    dosage_instruction VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 12. AI_CONSULTATION_LOGS (Nhật ký tư vấn AI)
-- ==========================================
CREATE TABLE IF NOT EXISTS ai_consultation_logs (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id) ON DELETE SET NULL,
    symptom_input TEXT NOT NULL,
    suggested_specialty_id INTEGER REFERENCES specialties(id) ON DELETE SET NULL,
    ai_reasoning TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- 13. INDEXES (Tối ưu hóa truy vấn)
-- ==========================================
CREATE INDEX IF NOT EXISTS idx_patients_code ON patients(patient_code);
CREATE INDEX IF NOT EXISTS idx_doctors_code ON doctors(doctor_code);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);
CREATE INDEX IF NOT EXISTS idx_medical_records_emr ON medical_records(emr_code);

-- ==========================================
-- INSERT SAMPLE DATA (Dữ liệu mẫu)
-- ==========================================

-- 1. Thêm chuyên khoa
INSERT INTO specialties (specialty_name, location) VALUES 
('Nội khoa', 'Tầng 2 - Khoa Nội'),
('Ngoài khoa', 'Tầng 3 - Khoa Ngoài'),
('Tâm lý', 'Tầng 4 - Khoa Tâm lý'),
('Ung bướu', 'Tầng 5 - Khoa Ung bướu'),
('Hồi sức cấp cứu', 'Tầng 1 - Khoa HSCCC')
ON CONFLICT DO NOTHING;

-- 2. Thêm danh mục bệnh (ICD-10)
INSERT INTO diseases (icd10_code, disease_name) VALUES 
('J45.9', 'Asthma, unspecified'),
('E11.9', 'Type 2 diabetes mellitus without complications'),
('I10', 'Essential (primary) hypertension'),
('K21.9', 'Unspecified reflux esophagitis'),
('F32.9', 'Major depressive disorder, single episode, unspecified'),
('M19.90', 'Unspecified osteoarthritis of unspecified site')
ON CONFLICT DO NOTHING;

-- 3. Thêm danh mục thuốc
INSERT INTO medicines (medicine_name, unit) VALUES 
('Paracetamol', 'Viên'),
('Ibuprofen', 'Viên'),
('Amoxicillin', 'Viên'),
('Loratadine', 'Viên'),
('Metformin', 'Viên'),
('Atorvastatin', 'Viên')
ON CONFLICT DO NOTHING;

-- 4. Thêm bệnh nhân (mẫu)
INSERT INTO patients (patient_code, full_name, dob, gender, phone, address) VALUES 
('P001', 'Nguyễn Văn A', '1990-01-15', 'MALE', '0912345678', '123 Đường Abc, TP HCM'),
('P002', 'Trần Thị B', '1995-05-20', 'FEMALE', '0987654321', '456 Đường Def, Hà Nội'),
('P003', 'Lê Văn C', '1988-03-10', 'MALE', '0911111111', '789 Đường Ghi, Đà Nẵng'),
('P004', 'Phạm Thị D', '1992-07-25', 'FEMALE', '0922222222', '101 Đường Jkl, TP HCM')
ON CONFLICT DO NOTHING;

-- 5. Thêm bác sĩ (mẫu)
INSERT INTO doctors (specialty_id, doctor_code, doctor_name, phone, degree, experience_years) VALUES 
(1, 'D001', 'Trần Văn X', '0933333333', 'MD, Internal Medicine', 10),
(2, 'D002', 'Nguyễn Thị Y', '0944444444', 'MD, Surgery', 8),
(3, 'D003', 'Lê Văn Z', '0955555555', 'MD, Psychiatry', 12),
(1, 'D004', 'Phạm Thị K', '0966666666', 'MD, Cardiology', 7)
ON CONFLICT DO NOTHING;

-- 6. Thêm lịch trực bác sĩ (mẫu)
INSERT INTO doctor_schedules (doctor_id, work_date, time_slot, is_booked) VALUES 
(1, '2026-06-20', '08:00-09:00', FALSE),
(1, '2026-06-20', '09:00-10:00', FALSE),
(1, '2026-06-21', '10:00-11:00', FALSE),
(2, '2026-06-20', '08:00-09:00', FALSE),
(2, '2026-06-20', '14:00-15:00', FALSE),
(3, '2026-06-21', '08:00-09:00', FALSE),
(4, '2026-06-22', '09:00-10:00', FALSE)
ON CONFLICT DO NOTHING;

-- 7. Thêm hẹn khám (mẫu)
INSERT INTO appointments (patient_id, doctor_id, appointment_date, time_slot, symptoms_initial, status) VALUES 
('P001', 1, '2026-06-20', '08:00-09:00', 'Đau đầu, sốt cao', 'WAITING'),
('P002', 2, '2026-06-20', '10:00-11:00', 'Đau bụng', 'WAITING'),
('P003', 1, '2026-06-21', '14:00-15:00', 'Khó thở', 'DONE'),
('P004', 3, '2026-06-22', '09:00-10:00', 'Stress, mất ngủ', 'CANCELLED')
ON CONFLICT DO NOTHING;

-- 8. Thêm bệnh án (mẫu)
INSERT INTO medical_records (emr_code, appointment_id, patient_id, doctor_id, diagnosis_icd10, clinical_note, history_summary, care_advice) VALUES 
('EMR001', 1, 'P001', 1, 'J45.9', 'Bệnh nhân ho kéo dài', 'Tiền sử ho hen', 'Kiêng lạnh, hạn chế hoạt động nặng'),
('EMR002', 2, 'P002', 2, 'K21.9', 'Bệnh nhân đau dạ dày', 'Ăn không điều độ', 'Ăn ít một lần, tránh thức ăn cay nóng'),
('EMR003', 3, 'P003', 1, 'E11.9', 'Bệnh nhân tiểu đường', 'Gia đình có tiểu đường', 'Kiên trì uống thuốc, kiểm tra đường huyết')
ON CONFLICT DO NOTHING;

-- 9. Thêm đơn thuốc (mẫu)
INSERT INTO prescriptions (medical_record_id, pdf_url) VALUES 
(1, 'https://example.com/prescription/001.pdf'),
(2, 'https://example.com/prescription/002.pdf'),
(3, 'https://example.com/prescription/003.pdf')
ON CONFLICT DO NOTHING;

-- 10. Thêm chi tiết đơn thuốc (mẫu)
INSERT INTO prescription_details (prescription_id, medicine_id, quantity, dosage_instruction) VALUES 
(1, 1, 2, 'Uống 1 viên 3 lần/ngày, sau ăn'),
(1, 3, 1, 'Uống 1 viên 2 lần/ngày trong 7 ngày'),
(2, 2, 2, 'Uống 1 viên 2 lần/ngày, sau ăn'),
(3, 5, 1, 'Uống 1 viên 1 lần/ngày, buổi sáng')
ON CONFLICT DO NOTHING;

-- 11. Thêm nhật ký AI (mẫu)
INSERT INTO ai_consultation_logs (patient_id, symptom_input, suggested_specialty_id, ai_reasoning) VALUES 
(1, 'Đau đầu, chóng mặt, mệt mỏi', 1, 'Có thể là thiếu máu hoặc bệnh tim mạch, cần khám nội khoa'),
(2, 'Đau bụng kéo dài, buồn nôn', 1, 'Có thể là viêm dạ dày, cần khám nội khoa'),
(3, 'Khó thở, hay bị sặc nước', 1, 'Có thể là hen phế quản, cần khám nội khoa'),
(4, 'Mất ngủ, lo âu, căng thẳng', 3, 'Có thể là rối loạn anxiety, cần khám tâm lý')
ON CONFLICT DO NOTHING;

-- ==========================================
-- ENABLE RLS (Row Level Security) - Tuỳ chọn
-- ==========================================
-- Bình luận lại các dòng sau nếu muốn bật RLS
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE doctors ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE medical_records ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE prescriptions ENABLE ROW LEVEL SECURITY;

-- ==========================================
-- VIEWS (Tuỳ chọn - Giúp truy vấn dễ hơn)
-- ==========================================

-- View: Lấy hẹn khám chờ xử lý
CREATE OR REPLACE VIEW waiting_appointments AS
SELECT 
    a.id,
    a.patient_id,
    p.full_name as patient_name,
    a.doctor_id,
    d.doctor_name,
    s.specialty_name,
    a.appointment_date,
    a.time_slot,
    a.symptoms_initial,
    a.status
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_code
JOIN doctors d ON a.doctor_id = d.id
JOIN specialties s ON d.specialty_id = s.id
WHERE a.status = 'WAITING';

-- View: Lịch trực còn trống
CREATE OR REPLACE VIEW available_doctor_slots AS
SELECT 
    ds.id,
    ds.doctor_id,
    d.doctor_name,
    s.specialty_name,
    ds.work_date,
    ds.time_slot,
    ds.is_booked
FROM doctor_schedules ds
JOIN doctors d ON ds.doctor_id = d.id
JOIN specialties s ON d.specialty_id = s.id
WHERE ds.is_booked = FALSE;

-- View: Thống kê hẹn khám theo trạng thái
CREATE OR REPLACE VIEW appointment_statistics AS
SELECT 
    status,
    COUNT(*) as count
FROM appointments
GROUP BY status;

COMMIT;
