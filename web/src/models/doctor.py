from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, ForeignKey
from src.database import Model
from typing import List
from .speciality import SpecialityOrm

doctor_specialities = Table(
    "doctor_specialities",
    Model.metadata,
    Column("doctor_id", ForeignKey("doctors.id"), primary_key=True),
    Column("speciality_id", ForeignKey("specialities.id"), primary_key=True)
)

class DoctorOrm(Model):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lastName: Mapped[str]
    firstName: Mapped[str]
    middleName: Mapped[str]
    workplace: Mapped[str]
    deleted: Mapped[bool] = mapped_column(default=False)
    
    specialities: Mapped[List[SpecialityOrm]] = relationship(
        "SpecialityOrm",
        secondary=doctor_specialities,
        back_populates="doctors"
    )

    orders: Mapped[List["OrderOrm"]] = relationship("OrderOrm", back_populates="doctor") 