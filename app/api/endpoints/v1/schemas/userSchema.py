from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import File, Form, UploadFile

class UserBase(BaseModel):
    fin_kod: str
    name: str
    surname: str
    father_name: str
    born_place: str
    living_location: str
    home_phone: str
    personal_mobile_number: str
    personal_email: EmailStr
    citizenship: str
    personal_id_number: str
    sex: str
    work_place: str
    department: str
    duty: str
    main_education: str
    additonal_education: Optional[str] = None
    scientific_degree: Optional[str] = None
    scientific_date: Optional[date] = None
    scientific_name: Optional[str] = None
    scientific_name_date: Optional[date] = None
    work_location: Optional[str] = None
    work_phone: Optional[str] = None
    work_email: Optional[EmailStr] = None
    born_date: str

class CreateUser(UserBase):
    fin_kod: str = Form(...)
    name: str = Form(...)
    surname: str = Form(...)
    father_name: str = Form(...)
    born_place: str = Form(...)
    living_location: str = Form(...)
    home_phone: str = Form(...)
    personal_mobile_number: str = Form(...)
    personal_email: str = Form(...)
    citizenship: str = Form(...)
    personal_id_number: str = Form(...)
    sex: str = Form(...)
    work_place: str = Form(...)
    department: str = Form(...)
    duty: str = Form(...)
    main_education: str = Form(...)
    additonal_education: str = Form(...)
    scientific_degree: str = Form(...)
    scientific_date: Optional[str] = Form(None)
    scientific_name: str = Form(...)
    scientific_name_date: Optional[str] = Form(None)
    work_location: str = Form(...)
    work_phone: str = Form(...)
    work_email: str = Form(...)
    born_date: str = Form(...)
    image: UploadFile = File(...)