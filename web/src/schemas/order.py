from pydantic import BaseModel
from datetime import date, time
from typing import List, Optional, ForwardRef

PatientRead = ForwardRef("PatientRead")

class SimpleDoctorRead(BaseModel):
    id: int
    lastName: str
    firstName: str
    middleName: str
    workplace: str
    deleted: bool

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    typeName: str  # Вид назначения
    title: str  # Название
    unit: str  # Единица измерения
    startDate: date  # Дата начала
    endDate: date  # Дата конца
    executionTimes: List[time]  # Время выполнения
    patientId: int  # ID пациента
    description: str  # Описание
    status: str  # Статус
    doctorId: int  # ID врача

class OrderRead(OrderCreate):
    orderId: int  # ID назначения, присвоенный БД
    patient: Optional[PatientRead] = None  # Информация о пациенте
    doctor: Optional[SimpleDoctorRead] = None  # Информация о враче (упрощенная)

    class Config:
        from_attributes = True

# Импортируем схемы после объявления
from src.schemas.patient import PatientRead

# Разрешаем опережающие ссылки
OrderRead.model_rebuild()
