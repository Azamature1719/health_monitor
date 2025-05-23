from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete
from src.models import AppointmentOrm
from typing import List
from datetime import date, time

class AppointmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_appointment(self, appointment_date: date, appointment_time: time, content: str, 
                             doctor_id: int, patient_id: int, service_id: int, status: str) -> int:
        appointment = AppointmentOrm(
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            content=content,
            doctor_id=doctor_id,
            patient_id=patient_id,
            service_id=service_id,
            status=status
        )
        self.session.add(appointment)
        await self.session.flush()
        await self.session.commit()
        return appointment.id

    async def update_appointment(self, appointment_id: int, appointment_date: date = None, 
                                appointment_time: time = None, content: str = None, 
                                doctor_id: int = None, patient_id: int = None, 
                                service_id: int = None, status: str = None):
        stmt = update(AppointmentOrm).where(AppointmentOrm.id == appointment_id)
        
        update_values = {}
        if appointment_date is not None:
            update_values["appointment_date"] = appointment_date
        if appointment_time is not None:
            update_values["appointment_time"] = appointment_time
        if content is not None:
            update_values["content"] = content
        if doctor_id is not None:
            update_values["doctor_id"] = doctor_id
        if patient_id is not None:
            update_values["patient_id"] = patient_id
        if service_id is not None:
            update_values["service_id"] = service_id
        if status is not None:
            update_values["status"] = status
            
        if update_values:
            stmt = stmt.values(**update_values)
            await self.session.execute(stmt)
            await self.session.commit()

    async def delete_appointment(self, appointment_id: int):
        stmt = delete(AppointmentOrm).where(AppointmentOrm.id == appointment_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_appointment_by_id(self, appointment_id: int) -> AppointmentOrm:
        query = select(AppointmentOrm).where(AppointmentOrm.id == appointment_id)
        result = await self.session.execute(query)
        appointment = result.scalars().one_or_none()
        return appointment

    async def get_all_appointments(self) -> List[AppointmentOrm]:
        query = select(AppointmentOrm)
        result = await self.session.execute(query)
        appointments = result.scalars().all()
        return appointments
        
    async def get_appointments_by_doctor(self, doctor_id: int) -> List[AppointmentOrm]:
        query = select(AppointmentOrm).where(AppointmentOrm.doctor_id == doctor_id)
        result = await self.session.execute(query)
        appointments = result.scalars().all()
        return appointments
        
    async def get_appointments_by_patient(self, patient_id: int) -> List[AppointmentOrm]:
        query = select(AppointmentOrm).where(AppointmentOrm.patient_id == patient_id)
        result = await self.session.execute(query)
        appointments = result.scalars().all()
        return appointments 