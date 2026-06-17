"""
API Endpoints Examples for Medical Management System
Ví dụ các endpoint API sử dụng Supabase database
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from supabase import create_client, Client

# Load environment variables from backend root .env file
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(dotenv_path=env_path)

class SupabaseDB:
    """Database connection wrapper for Supabase"""

    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.url, self.key)

    def select(self, table: str, columns: str = "*", limit: int = 100):
        try:
            response = self.client.table(table).select(columns).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error selecting from {table}: {e}")
            return None

    def select_where(self, table: str, column: str, value, columns: str = "*"):
        try:
            response = self.client.table(table).select(columns).eq(column, value).execute()
            return response.data
        except Exception as e:
            print(f"Error querying {table}: {e}")
            return None

    def insert(self, table: str, data: dict):
        try:
            response = self.client.table(table).insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error inserting into {table}: {e}")
            return None

    def update(self, table: str, data: dict, filter_column: str, filter_value):
        try:
            response = self.client.table(table).update(data).eq(filter_column, filter_value).execute()
            return response.data
        except Exception as e:
            print(f"Error updating {table}: {e}")
            return None

    def delete(self, table: str, filter_column: str, filter_value):
        try:
            response = self.client.table(table).delete().eq(filter_column, filter_value).execute()
            return response.data
        except Exception as e:
            print(f"Error deleting from {table}: {e}")
            return None

# Initialize Supabase client

try:
    db = SupabaseDB()
except Exception as e:
    print(f"Failed to initialize Supabase client: {e}")
    db = None

app = Flask(__name__)

# ============================================================
# PATIENTS - Quản lý bệnh nhân (MC-01, MC-02)
# ============================================================

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Lấy danh sách bệnh nhân"""
    try:
        limit = request.args.get('limit', 10, type=int)
        patients = db.select('patients', limit=limit)
        return jsonify({
            'success': True,
            'data': patients,
            'count': len(patients) if patients else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/patients/<patient_code>', methods=['GET'])
def get_patient(patient_code):
    """Lấy thông tin bệnh nhân theo mã"""
    try:
        patient = db.select_where('patients', 'patient_code', patient_code)
        if patient:
            return jsonify({
                'success': True,
                'data': patient[0]
            })
        return jsonify({
            'success': False,
            'error': 'Patient not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/patients', methods=['POST'])
def create_patient():
    """Tạo bệnh nhân mới"""
    try:
        data = request.json
        patient = db.insert('patients', data)
        return jsonify({
            'success': True,
            'data': patient[0] if patient else None
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================
# DOCTORS - Quản lý bác sĩ (MC-03)
# ============================================================

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Lấy danh sách bác sĩ"""
    try:
        limit = request.args.get('limit', 10, type=int)
        doctors = db.select('doctors', limit=limit)
        return jsonify({
            'success': True,
            'data': doctors,
            'count': len(doctors) if doctors else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/doctors/<doctor_code>', methods=['GET'])
def get_doctor(doctor_code):
    """Lấy thông tin bác sĩ theo mã"""
    try:
        doctor = db.select_where('doctors', 'doctor_code', doctor_code)
        if doctor:
            return jsonify({
                'success': True,
                'data': doctor[0]
            })
        return jsonify({
            'success': False,
            'error': 'Doctor not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================
# USERS - Quản lý tài khoản (Supabase Auth)
# ============================================================

@app.route('/api/users', methods=['GET'])
def get_users():
    """Lấy danh sách người dùng"""
    try:
        users = db.select('users', limit=request.args.get('limit', 20, type=int))
        return jsonify({
            'success': True,
            'data': users,
            'count': len(users) if users else 0
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Lấy người dùng theo ID"""
    try:
        user = db.select_where('users', 'id', user_id)
        if user:
            return jsonify({'success': True, 'data': user[0]})
        return jsonify({'success': False, 'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/users', methods=['POST'])
def create_user():
    """Thêm người dùng mới"""
    try:
        data = request.json
        user = db.insert('users', data)
        return jsonify({'success': True, 'data': user[0] if user else None}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============================================================
# SPECIALTIES - Chuyên khoa
# ============================================================

@app.route('/api/specialties', methods=['GET'])
def get_specialties():
    """Lấy danh sách chuyên khoa"""
    try:
        specialties = db.select('specialties', limit=request.args.get('limit', 20, type=int))
        return jsonify({
            'success': True,
            'data': specialties,
            'count': len(specialties) if specialties else 0
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/specialties/<int:specialty_id>', methods=['GET'])
def get_specialty(specialty_id):
    """Lấy chuyên khoa theo ID"""
    try:
        specialty = db.select_where('specialties', 'id', specialty_id)
        if specialty:
            return jsonify({'success': True, 'data': specialty[0]})
        return jsonify({'success': False, 'error': 'Specialty not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/specialties', methods=['POST'])
def create_specialty():
    """Thêm chuyên khoa mới"""
    try:
        data = request.json
        specialty = db.insert('specialties', data)
        return jsonify({'success': True, 'data': specialty[0] if specialty else None}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============================================================
# DISEASES - Danh mục bệnh
# ============================================================

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Lấy danh sách bệnh"""
    try:
        diseases = db.select('diseases', limit=request.args.get('limit', 20, type=int))
        return jsonify({
            'success': True,
            'data': diseases,
            'count': len(diseases) if diseases else 0
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/diseases/<icd10_code>', methods=['GET'])
def get_disease(icd10_code):
    """Lấy bệnh theo mã ICD-10"""
    try:
        disease = db.select_where('diseases', 'icd10_code', icd10_code)
        if disease:
            return jsonify({'success': True, 'data': disease[0]})
        return jsonify({'success': False, 'error': 'Disease not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/diseases', methods=['POST'])
def create_disease():
    """Thêm bệnh mới"""
    try:
        data = request.json
        disease = db.insert('diseases', data)
        return jsonify({'success': True, 'data': disease[0] if disease else None}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============================================================
# MEDICINES - Danh mục thuốc
# ============================================================

@app.route('/api/medicines', methods=['GET'])
def get_medicines():
    """Lấy danh sách thuốc"""
    try:
        medicines = db.select('medicines', limit=request.args.get('limit', 20, type=int))
        return jsonify({
            'success': True,
            'data': medicines,
            'count': len(medicines) if medicines else 0
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine(medicine_id):
    """Lấy thuốc theo ID"""
    try:
        medicine = db.select_where('medicines', 'id', medicine_id)
        if medicine:
            return jsonify({'success': True, 'data': medicine[0]})
        return jsonify({'success': False, 'error': 'Medicine not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/medicines', methods=['POST'])
def create_medicine():
    """Thêm thuốc mới"""
    try:
        data = request.json
        medicine = db.insert('medicines', data)
        return jsonify({'success': True, 'data': medicine[0] if medicine else None}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============================================================
# PRESCRIPTION DETAILS - Chi tiết đơn thuốc
# ============================================================

@app.route('/api/prescription-details', methods=['GET'])
def get_prescription_details():
    """Lấy chi tiết đơn thuốc"""
    try:
        prescription_id = request.args.get('prescription_id', type=int)
        if prescription_id:
            details = db.select_where('prescription_details', 'prescription_id', prescription_id)
        else:
            details = db.select('prescription_details', limit=20)
        return jsonify({
            'success': True,
            'data': details,
            'count': len(details) if details else 0
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/prescription-details', methods=['POST'])
def create_prescription_detail():
    """Thêm chi tiết đơn thuốc"""
    try:
        data = request.json
        detail = db.insert('prescription_details', data)
        return jsonify({'success': True, 'data': detail[0] if detail else None}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============================================================
# DOCTOR SCHEDULES - Lịch trực (MC-04)
# ============================================================

@app.route('/api/doctor-schedules', methods=['GET'])
def get_doctor_schedules():
    """Lấy lịch trực của bác sĩ"""
    try:
        doctor_id = request.args.get('doctor_id', type=int)
        is_booked = request.args.get('is_booked', type=lambda x: x.lower() == 'true')
        
        if doctor_id:
            schedules = db.select_where('doctor_schedules', 'doctor_id', doctor_id)
        elif is_booked is not None:
            schedules = db.select_where('doctor_schedules', 'is_booked', is_booked)
        else:
            schedules = db.select('doctor_schedules', limit=20)
        
        return jsonify({
            'success': True,
            'data': schedules,
            'count': len(schedules) if schedules else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/doctor-schedules/available', methods=['GET'])
def get_available_slots():
    """Lấy các slot chưa được đặt"""
    try:
        available = db.select_where('doctor_schedules', 'is_booked', False)
        return jsonify({
            'success': True,
            'data': available,
            'count': len(available) if available else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/doctor-schedules', methods=['POST'])
def create_doctor_schedule():
    """Tạo lịch trực bác sĩ mới"""
    try:
        data = request.json
        schedule = db.insert('doctor_schedules', data)
        return jsonify({'success': True, 'data': schedule[0] if schedule else None}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============================================================
# APPOINTMENTS - Hẹn khám (MC-05, MC-08, MC-14)
# ============================================================

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Lấy danh sách hẹn khám"""
    try:
        status = request.args.get('status')
        patient_id = request.args.get('patient_id')
        
        if status:
            appointments = db.select_where('appointments', 'status', status)
        elif patient_id:
            appointments = db.select_where('appointments', 'patient_id', patient_id)
        else:
            appointments = db.select('appointments', limit=20)
        
        return jsonify({
            'success': True,
            'data': appointments,
            'count': len(appointments) if appointments else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/appointments/waiting', methods=['GET'])
def get_waiting_appointments():
    """Lấy danh sách hẹn khám chờ xử lý (MC-08)"""
    try:
        waiting = db.select_where('appointments', 'status', 'WAITING')
        return jsonify({
            'success': True,
            'data': waiting,
            'count': len(waiting) if waiting else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    """Tạo hẹn khám mới (MC-05)"""
    try:
        data = request.json
        
        # Tạo hẹn khám
        appointment = db.insert('appointments', data)
        
        # Nếu có schedule_id, đánh dấu slot đã được đặt
        if 'schedule_id' in data:
            db.update('doctor_schedules', {
                'is_booked': True
            }, 'id', data['schedule_id'])
        
        return jsonify({
            'success': True,
            'data': appointment[0] if appointment else None
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/appointments/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Cập nhật trạng thái hẹn khám (MC-08)"""
    try:
        data = request.json
        updated = db.update('appointments', data, 'id', int(appointment_id))
        
        return jsonify({
            'success': True,
            'data': updated[0] if updated else None
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================
# MEDICAL RECORDS - Bệnh án (MC-06)
# ============================================================

@app.route('/api/medical-records', methods=['GET'])
def get_medical_records():
    """Lấy danh sách bệnh án"""
    try:
        patient_id = request.args.get('patient_id')
        doctor_id = request.args.get('doctor_id', type=int)
        
        if patient_id:
            records = db.select_where('medical_records', 'patient_id', patient_id)
        elif doctor_id:
            records = db.select_where('medical_records', 'doctor_id', doctor_id)
        else:
            records = db.select('medical_records', limit=20)
        
        return jsonify({
            'success': True,
            'data': records,
            'count': len(records) if records else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/medical-records', methods=['POST'])
def create_medical_record():
    """Tạo bệnh án mới (MC-06)"""
    try:
        data = request.json
        record = db.insert('medical_records', data)
        
        return jsonify({
            'success': True,
            'data': record[0] if record else None
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================
# PRESCRIPTIONS - Đơn thuốc (MC-07)
# ============================================================

@app.route('/api/prescriptions', methods=['GET'])
def get_prescriptions():
    """Lấy danh sách đơn thuốc"""
    try:
        medical_record_id = request.args.get('medical_record_id', type=int)
        
        if medical_record_id:
            prescriptions = db.select_where('prescriptions', 'medical_record_id', medical_record_id)
        else:
            prescriptions = db.select('prescriptions', limit=20)
        
        return jsonify({
            'success': True,
            'data': prescriptions,
            'count': len(prescriptions) if prescriptions else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/prescriptions', methods=['POST'])
def create_prescription():
    """Tạo đơn thuốc mới (MC-07)"""
    try:
        data = request.json
        prescription = db.insert('prescriptions', data)
        
        return jsonify({
            'success': True,
            'data': prescription[0] if prescription else None
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================
# AI CONSULTATION LOGS - Nhật ký AI (MC-12)
# ============================================================

@app.route('/api/ai-logs', methods=['GET'])
def get_ai_logs():
    """Lấy nhật ký tư vấn AI"""
    try:
        patient_id = request.args.get('patient_id', type=int)
        
        if patient_id:
            logs = db.select_where('ai_consultation_logs', 'patient_id', patient_id)
        else:
            logs = db.select('ai_consultation_logs', limit=20)
        
        return jsonify({
            'success': True,
            'data': logs,
            'count': len(logs) if logs else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/ai-logs', methods=['POST'])
def create_ai_log():
    """Tạo nhật ký AI mới (MC-12)"""
    try:
        data = request.json
        log = db.insert('ai_consultation_logs', data)
        
        return jsonify({
            'success': True,
            'data': log[0] if log else None
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================
# STATISTICS - Thống kê (MC-14)
# ============================================================

@app.route('/api/statistics/appointments', methods=['GET'])
def get_appointment_statistics():
    """Thống kê hẹn khám theo trạng thái (MC-14)"""
    try:
        waiting = db.select_where('appointments', 'status', 'WAITING')
        in_progress = db.select_where('appointments', 'status', 'IN_PROGRESS')
        done = db.select_where('appointments', 'status', 'DONE')
        cancelled = db.select_where('appointments', 'status', 'CANCELLED')
        
        return jsonify({
            'success': True,
            'data': {
                'waiting': len(waiting) if waiting else 0,
                'in_progress': len(in_progress) if in_progress else 0,
                'done': len(done) if done else 0,
                'cancelled': len(cancelled) if cancelled else 0,
                'total': (len(waiting) if waiting else 0) + 
                         (len(in_progress) if in_progress else 0) + 
                         (len(done) if done else 0) + 
                         (len(cancelled) if cancelled else 0)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/statistics/doctors', methods=['GET'])
def get_doctor_statistics():
    """Thống kê bác sĩ"""
    try:
        doctors = db.select('doctors', limit=1000)
        specialties_count = {}
        
        if doctors:
            for doctor in doctors:
                spec_id = doctor.get('specialty_id')
                if spec_id:
                    specialties_count[spec_id] = specialties_count.get(spec_id, 0) + 1
        
        return jsonify({
            'success': True,
            'data': {
                'total_doctors': len(doctors) if doctors else 0,
                'by_specialty': specialties_count
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("Starting Medical Management System API")
    print("✓ Available endpoints:")
    print("  GET  /api/users")
    print("  GET  /api/users/<user_id>")
    print("  POST /api/users")
    print("  GET  /api/specialties")
    print("  GET  /api/specialties/<id>")
    print("  POST /api/specialties")
    print("  GET  /api/diseases")
    print("  GET  /api/diseases/<icd10_code>")
    print("  POST /api/diseases")
    print("  GET  /api/medicines")
    print("  GET  /api/medicines/<id>")
    print("  POST /api/medicines")
    print("  GET  /api/patients")
    print("  GET  /api/patients/<patient_code>")
    print("  POST /api/patients")
    print("  GET  /api/doctors")
    print("  GET  /api/doctors/<doctor_code>")
    print("  GET  /api/doctor-schedules")
    print("  GET  /api/doctor-schedules/available")
    print("  POST /api/doctor-schedules")
    print("  GET  /api/appointments")
    print("  GET  /api/appointments/waiting")
    print("  POST /api/appointments")
    print("  PUT  /api/appointments/<appointment_id>")
    print("  GET  /api/medical-records")
    print("  POST /api/medical-records")
    print("  GET  /api/prescriptions")
    print("  POST /api/prescriptions")
    print("  GET  /api/prescription-details")
    print("  POST /api/prescription-details")
    print("  GET  /api/ai-logs")
    print("  POST /api/ai-logs")
    print("  GET  /api/statistics/appointments")
    print("  GET  /api/statistics/doctors")
    
    app.run(debug=True, port=5000)
