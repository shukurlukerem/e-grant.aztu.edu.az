from pydantic import BaseModel
from typing import Optional

class RentCreateSchema(BaseModel):
    project_code: int
    rent_area: str
    unit_of_measure: str
    unit_price: int
    quantity: int
    duration: int
    total_amount: int

class RentUpdateSchema(BaseModel):
    id: int
    rent_area: Optional[str] = None
    unit_of_measure: Optional[str] = None
    unit_price: Optional[int] = None
    quantity: Optional[int] = None
    duration: Optional[int] = None

class RentResponseSchema(RentCreateSchema):
    id: int

    class Config:
        orm_mode = True
