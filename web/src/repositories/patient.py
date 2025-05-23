from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from src.models import PatientOrm
from typing import List
from datetime import date

class PatientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_patient(self, last_name: str, first_name: str, middle_name: str, birth_date: date, city: str, additional_info: str = None) -> int:
        patient = PatientOrm(lastName=last_name, firstName=first_name, middleName=middle_name, birthDate=birth_date, city=city, additionalInfo=additional_info)
        self.session.add(patient)
        await self.session.flush()
        await self.session.commit()
        return patient.id

    async def update_patient(self, patient_id: int, last_name: str = None, first_name: str = None, middle_name: str = None, birth_date: date = None, city: str = None, additional_info: str = None):
        stmt = update(PatientOrm).where(PatientOrm.id == patient_id)
        if last_name is not None:
            stmt = stmt.values(lastName=last_name)
        if first_name is not None:
            stmt = stmt.values(firstName=first_name)
        if middle_name is not None:
            stmt = stmt.values(middleName=middle_name)
        if birth_date is not None:
            stmt = stmt.values(birthDate=birth_date)
        if city is not None:
            stmt = stmt.values(city=city)
        if additional_info is not None:
            stmt = stmt.values(additionalInfo=additional_info)
        await self.session.execute(stmt)
        await self.session.commit()

    async def mark_patient_deleted(self, patient_id: int):
        stmt = update(PatientOrm).where(PatientOrm.id == patient_id).values(deleted=True)
        await self.session.execute(stmt)
        await self.session.commit()

    async def restore_patient(self, patient_id: int):
        stmt = update(PatientOrm).where(PatientOrm.id == patient_id).values(deleted=False)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_patient_by_id(self, patient_id: int) -> PatientOrm:
        query = select(PatientOrm).where(PatientOrm.id == patient_id)
        result = await self.session.execute(query)
        patient = result.scalars().one_or_none()
        return patient

    async def get_all_patients(self) -> List[PatientOrm]:
        query = select(PatientOrm)
        result = await self.session.execute(query)
        patients = result.scalars().all()
        return patients 