from pydantic import BaseModel
from datetime import datetime

class ResultCreate(BaseModel):
    resultIdMobile: int = 1 # ID индикатора в мобильном приложении
    orderId: int  # Связь с назначением
    patientId: int
    doctorId: int
    typeName: str
    title: str
    unit: str      
    executionTime: datetime
    value: float
    status: str

class ResultRead(ResultCreate):
    id: int # ID индикатора, присвоенный БД 