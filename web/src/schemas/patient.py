from pydantic import BaseModel
from datetime import date
from typing import List, Optional, ForwardRef

OrderRead = ForwardRef("OrderRead")

class PatientCreate(BaseModel):
    lastName: str
    firstName: str
    middleName: str
    birthDate: date
    city: str
    additionalInfo: str = None

class PatientRead(PatientCreate):
    id: int
    deleted: bool

    class Config:
        from_attributes = True
        populate_by_name = True 