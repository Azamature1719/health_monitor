from pydantic import BaseModel
from typing import List, Optional, ForwardRef
from .speciality import SpecialityRead

OrderRead = ForwardRef("OrderRead")

class DoctorCreate(BaseModel):
    lastName: str
    firstName: str
    middleName: str
    workplace: str
    speciality_ids: Optional[List[int]] = None

class Config:
    from_attributes = True
    populate_by_name = True

class DoctorRead(DoctorCreate):
    id: int
    deleted: bool
    specialities: Optional[List[SpecialityRead]] = None

    class Config:
        from_attributes = True
        populate_by_name = True 