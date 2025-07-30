from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserProfileUpdate(BaseModel):
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
