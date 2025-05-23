from src.database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class SpecialityOrm(Model):
    __tablename__ = 'specialities'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    
    # Обратное отношение к врачам
    doctors: Mapped[List["DoctorOrm"]] = relationship(
        "DoctorOrm",
        secondary="doctor_specialities",
        back_populates="specialities"
    ) 