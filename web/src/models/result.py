from src.database import Model
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, TIMESTAMP
from datetime import datetime

class ResultOrm(Model):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resultIdMobile: Mapped[int]
    title: Mapped[str]
    typeName: Mapped[str]
    patientId: Mapped[int]
    executionTime: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    value: Mapped[float]
    unit: Mapped[str]
    status: Mapped[str]
    orderId: Mapped[int] = mapped_column(ForeignKey("orders.orderId"))
    doctorId: Mapped[int]