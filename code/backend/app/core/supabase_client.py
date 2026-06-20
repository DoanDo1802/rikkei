import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseDB:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        if not self.url or not self.key:
            raise ValueError("Thiếu SUPABASE_URL hoặc SUPABASE_KEY trong file .env")
        self.client: Client = create_client(self.url, self.key)

    # Hàm SELECT dùng chung (từ file api.py cũ của bạn)
    def select(self, table: str, columns: str = "*", limit: int = 100):
        response = self.client.table(table).select(columns).limit(limit).execute()
        return response.data

    # Hàm INSERT dùng chung
    def insert(self, table: str, data: dict):
        response = self.client.table(table).insert(data).execute()
        return response.data

# Khởi tạo instance dùng cho toàn bộ backend
db = SupabaseDB()