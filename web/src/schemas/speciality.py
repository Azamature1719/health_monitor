from pydantic import BaseModel

class SpecialityCreate(BaseModel):
    name: str

class SpecialityRead(SpecialityCreate):
    id: int

    class Config:
        from_attributes = True 