from fastapi import APIRouter, HTTPException,  Depends
from app.schemas.request.auth import PatientRegisterRequest
from app.core.supabase_client import db
from app.services.id_generator import generate_patient_code

router = APIRouter()

@router.post("/register/patient")
async def register_patient(payload: PatientRegisterRequest):
    try:
        # 1. Đăng ký tài khoản vào Supabase Auth
        auth_res = db.client.auth.sign_up({
            "email": payload.email, 
            "password": payload.password
        })
        
        if not auth_res.user:
            raise HTTPException(status_code=400, detail="Đăng ký tài khoản thất bại")
        
        user_id = auth_res.user.id
        
        # 2. Lưu vào bảng public.users (Phân quyền)
        db.insert("users", {"id": user_id, "role": "PATIENT"})
        
        # 3. Sinh mã và Lưu vào bảng public.patients
        p_code = await generate_patient_code()
        db.insert("patients", {
            "user_id": user_id,
            "patient_code": p_code,
            "full_name": payload.full_name,
            "phone": payload.phone
        })
        
        return {"status": "success", "patient_code": p_code}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
from pydantic import BaseModel, EmailStr

# Định nghĩa dữ liệu yêu cầu đăng nhập
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(payload: LoginRequest):
    try:
        # 1. Gọi Supabase Auth để kiểm tra email/mật khẩu
        res = db.client.auth.sign_in_with_password({
            "email": payload.email, 
            "password": payload.password
        })
        
        if not res.session:
            raise HTTPException(status_code=401, detail="Sai thông tin đăng nhập")
        
        # 2. Truy vấn role từ bảng users để trả về cho Frontend
        user_id = res.user.id
        user_data = db.client.table("users").select("role").eq("id", user_id).single().execute()
        
        # 3. Trả về Token và thông tin cơ bản
        return {
            "status": "success",
            "access_token": res.session.access_token,
            "token_type": "bearer",
            "user_info": {
                "id": user_id,
                "email": res.user.email,
                "role": user_data.data["role"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
from app.core.security import get_current_user

@router.get("/me")
async def get_my_info(user: dict = Depends(get_current_user)):
    return {"message": "Bạn đã đăng nhập thành công", "user": user}