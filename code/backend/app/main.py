from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

app = FastAPI(title="MediCore API System")

# 2. Cấu hình CORS
# Danh sách các nguồn (Frontend) được phép gọi tới API này
origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Cho phép các nguồn trong danh sách trên
    allow_credentials=True,     # Cho phép gửi Cookies/Auth headers
    allow_methods=["*"],        # Cho phép tất cả các lệnh GET, POST, PUT, DELETE...
    allow_headers=["*"],        # Cho phép tất cả các loại Header
)

# 3. Khai báo Router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hệ thống API Y tế Rikkei đang hoạt động!"}