from pydantic import BaseModel, EmailStr

class PatientRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: str