from pydantic import BaseModel
from typing import Optional

class SubjectBase(BaseModel):
    equipment_name: str
    unit_of_measure: str
    price: int
    quantity: int

class SubjectCreate(BaseModel):
    project_code: int
    fin_code: str
    equipment_name: str
    unit_of_measure: str
    price: int
    quantity: int

class SubjectUpdate(BaseModel):
    equipment_name: Optional[str]
    unit_of_measure: Optional[str]
    price: Optional[int]
    quantity: Optional[int]

class SubjectResponse(SubjectBase):
    id: int
    project_code: int
    total_amount: int
