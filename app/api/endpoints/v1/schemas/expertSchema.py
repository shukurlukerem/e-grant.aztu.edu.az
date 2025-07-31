from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from pydantic import BaseModel, validator
import phonenumbers

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

    @validator('phone_number')
    def validate_phone_number(cls, value: str) -> str:
        try:
            parsed_number = phonenumbers.parse(value, None)
        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format")

        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")

        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)


#### gmail validator

    class Config:
        orm_mode = True


class ExpertCreate(ExpertBase):
    pass


class ExpertOut(ExpertBase):
    id: int
