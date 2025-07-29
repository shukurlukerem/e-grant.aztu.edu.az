from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class ExpertBase(BaseModel):
    email: EmailStr
    name: str
    surname: str
    father_name: str
    personal_id_serial_number: str
    work_place: Optional[str] = None
    duty: Optional[str] = None
    scientific_degree: Optional[str] = None
    phone_number: str

    class Config:
        orm_mode = True


class ExpertCreate(ExpertBase):
    pass


class ExpertOut(ExpertBase):
    id: int
