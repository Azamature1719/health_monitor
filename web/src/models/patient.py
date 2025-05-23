from src.database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List

class PatientOrm(Model):
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(primary_key=True)
    lastName: Mapped[str]
    firstName: Mapped[str]
    middleName: Mapped[str]
    birthDate: Mapped[date]
    city: Mapped[str]
    additionalInfo: Mapped[str] = mapped_column(nullable=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    
    orders: Mapped[List["OrderOrm"]] = relationship("OrderOrm", back_populates="patient") 