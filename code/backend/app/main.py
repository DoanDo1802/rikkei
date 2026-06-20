from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(title="MediCore API System")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hệ thống API Y tế Rikkei đang hoạt động!"}