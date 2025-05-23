from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIME, ForeignKey
from datetime import date, time
from typing import List
from sqlalchemy.dialects.postgresql import ARRAY

from src.database import Model
from src.models.patient import PatientOrm
from src.models.doctor import DoctorOrm

class OrderOrm(Model):  
    __tablename__ = "orders"

    patientId: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    doctorId: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    orderId: Mapped[int] = mapped_column(primary_key=True)
    typeName: Mapped[str]
    title: Mapped[str]
    unit: Mapped[str]
    startDate: Mapped[date]
    endDate: Mapped[date]
    executionTimes: Mapped[List[time]] = mapped_column(ARRAY(TIME))
    description: Mapped[str]
    status: Mapped[str]
    
    patient: Mapped["PatientOrm"] = relationship("PatientOrm", back_populates="orders")
    doctor: Mapped["DoctorOrm"] = relationship("DoctorOrm", back_populates="orders")