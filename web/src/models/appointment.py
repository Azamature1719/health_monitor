from src.database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import date, time

class AppointmentOrm(Model):
    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_date: Mapped[date]
    appointment_time: Mapped[time]
    content: Mapped[str] = mapped_column(nullable=True)
    
    # Внешние ключи
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    
    # Статус
    status: Mapped[str] 