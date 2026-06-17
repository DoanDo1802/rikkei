-- 1. Bảng Chuyên khoa (MC-04)
CREATE TABLE specialties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    specialty_name VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Bảng Tài khoản người dùng (MC-03)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'DOCTOR', 'PATIENT') NOT NULL
);

-- 3. Bảng Hồ sơ Bệnh nhân (MC-03, MC-15)
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    patient_code VARCHAR(20) NOT NULL UNIQUE, -- PAT-YYYY-NNNN
    full_name VARCHAR(100) NOT NULL,
    dob DATE,
    gender ENUM('MALE', 'FEMALE', 'OTHER'),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 4. Bảng Hồ sơ Bác sĩ (MC-04)
CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    specialty_id INT,
    doctor_code VARCHAR(20) NOT NULL UNIQUE, -- DOC-NNNN
    doctor_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (specialty_id) REFERENCES specialties(id)
);

-- 5. Bảng Lịch hẹn (MC-06, MC-08)
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(20), -- Lưu patient_code
    doctor_id INT,
    appointment_date DATE NOT NULL,
    time_slot VARCHAR(50) NOT NULL,
    symptoms_initial TEXT,
    status ENUM('WAITING', 'IN_PROGRESS', 'DONE', 'CANCELLED') DEFAULT 'WAITING',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_code),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- 6. Danh mục Thuốc và Mã bệnh (MC-05)
CREATE TABLE medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_name VARCHAR(100) NOT NULL,
    unit VARCHAR(20) NOT NULL
);

CREATE TABLE diseases (
    icd10_code VARCHAR(10) PRIMARY KEY,
    disease_name VARCHAR(255) NOT NULL
);

-- 7. Hồ sơ bệnh án (MC-09, MC-13, MC-15)
CREATE TABLE medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emr_code VARCHAR(20) NOT NULL UNIQUE, -- EMR-YYYYMMDD-NN
    appointment_id INT,
    patient_id VARCHAR(20), -- Lưu patient_code để AI truy vấn lịch sử
    doctor_id INT,
    diagnosis_icd10 VARCHAR(10),
    clinical_note TEXT,
    history_summary TEXT, -- Kết quả AI tóm tắt (MC-13)
    care_advice TEXT,     -- Kết quả AI lời dặn (MC-13)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_code),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (diagnosis_icd10) REFERENCES diseases(icd10_code)
);

-- 8. Đơn thuốc và Chi tiết (MC-10)
CREATE TABLE prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medical_record_id INT,
    pdf_url VARCHAR(255),
    FOREIGN KEY (medical_record_id) REFERENCES medical_records(id)
);

CREATE TABLE prescription_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prescription_id INT,
    medicine_id INT,
    quantity INT,
    dosage_instruction VARCHAR(255),
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
);