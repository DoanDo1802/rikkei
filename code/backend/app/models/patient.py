from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    patient_code: str = Field(unique=True) # PAT-YYYY-XXXX
    full_name: str
    phone: str
    dob: Optional[date] = None
    gender: Optional[str] = None