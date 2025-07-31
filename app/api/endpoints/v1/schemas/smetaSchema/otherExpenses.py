from pydantic import BaseModel
from typing import Optional

class OtherExpCreate(BaseModel):
    project_code: int
    expenses_name: str
    unit_of_measure: str
    unit_price: int  # str olmalıdır, çünki modeldə String-dir
    quantity: int
    duration: int
    total_amount: int   # int olmalıdır, çünki modeldə Integer-dir

class OtherExpUpdate(BaseModel):
    project_code: Optional[int] = None
    expenses_name: Optional[str] = None
    unit_of_measure: Optional[str] = None
    unit_price: Optional[int] = None
    quantity: Optional[int] = None
    duration: Optional[int] = None
    total_amount: Optional[int] = None
