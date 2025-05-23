from pydantic import BaseModel

class ServiceCreate(BaseModel):
    name: str

class ServiceRead(ServiceCreate):
    id: int

    class Config:
        from_attributes = True 