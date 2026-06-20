from enum import Enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"

class User(SQLModel, table=True):
    id: str = Field(primary_key=True) # UUID từ Supabase Auth
    role: UserRole
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)# User database entity model placeholder
