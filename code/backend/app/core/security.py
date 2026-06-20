from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # Thêm cái này
from app.core.supabase_client import db

# Sửa dòng này: Thay OAuth2PasswordBearer bằng HTTPBearer
security = HTTPBearer()

async def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    # Lấy token từ header "Authorization: Bearer <token>"
    token = auth.credentials 
    
    try:
        # 1. Gọi Supabase Auth để xác thực Token này
        user_res = db.client.auth.get_user(token)
        if not user_res.user:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
        
        # 2. Lấy role của user từ bảng public.users
        user_id = user_res.user.id
        user_data = db.client.table("users").select("role").eq("id", user_id).single().execute()
        
        return {
            "id": user_id,
            "email": user_res.user.email,
            "role": user_data.data["role"]
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Xác thực thất bại hoặc Token hết hạn")

# Hàm kiểm tra quyền Admin
def verify_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Chỉ Admin mới có quyền này")
    return current_user