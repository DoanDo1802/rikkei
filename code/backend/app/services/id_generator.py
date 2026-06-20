import datetime
from app.core.supabase_client import db

async def generate_patient_code():
    year = datetime.datetime.now().year
    # Đếm số lượng bệnh nhân để tăng số thứ tự
    data = db.select("patients", columns="id")
    count = len(data) + 1 if data else 1
    return f"PAT-{year}-{count:04d}"