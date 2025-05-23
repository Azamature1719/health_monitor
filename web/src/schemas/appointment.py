from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class AppointmentCreate(BaseModel):
    appointment_date: date
    appointment_time: time
    content: Optional[str] = None
    doctor_id: int
    patient_id: int
    service_id: int
    status: str

class AppointmentRead(AppointmentCreate):
    id: int

    class Config:
        from_attributes = True 