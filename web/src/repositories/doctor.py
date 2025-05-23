from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from src.models import DoctorOrm, SpecialityOrm
from src.models.doctor import doctor_specialities
from typing import List, Optional
import sqlalchemy.orm

class DoctorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_doctor(self, last_name: str, first_name: str, middle_name: str, workplace: str, speciality_ids: Optional[List[int]] = None) -> int:
        doctor = DoctorOrm(lastName=last_name, firstName=first_name, middleName=middle_name, workplace=workplace)
        
        # Если переданы специализации, добавляем их к врачу
        if speciality_ids:
            specialities = await self._get_specialities_by_ids(speciality_ids)
            doctor.specialities = specialities
            
        self.session.add(doctor)
        await self.session.flush()
        await self.session.commit()
        return doctor.id

    async def update_doctor(self, doctor_id: int, last_name: str = None, first_name: str = None, middle_name: str = None, workplace: str = None, speciality_ids: Optional[List[int]] = None):
        doctor = await self.get_doctor_by_id(doctor_id)
        if not doctor:
            return
            
        if last_name is not None:
            doctor.lastName = last_name
        if first_name is not None:
            doctor.firstName = first_name
        if middle_name is not None:
            doctor.middleName = middle_name
        if workplace is not None:
            doctor.workplace = workplace
            
        # Если переданы специализации, обновляем их
        if speciality_ids is not None:
            specialities = await self._get_specialities_by_ids(speciality_ids)
            doctor.specialities = specialities
            
        await self.session.commit()

    async def _get_specialities_by_ids(self, speciality_ids: List[int]) -> List[SpecialityOrm]:
        if not speciality_ids:
            return []
            
        query = select(SpecialityOrm).where(SpecialityOrm.id.in_(speciality_ids))
        result = await self.session.execute(query)
        specialities = result.scalars().all()
        return specialities

    async def mark_doctor_deleted(self, doctor_id: int):
        stmt = update(DoctorOrm).where(DoctorOrm.id == doctor_id).values(deleted=True)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_doctor_by_id(self, doctor_id: int) -> DoctorOrm:
        query = select(DoctorOrm).where(DoctorOrm.id == doctor_id).options(
            sqlalchemy.orm.selectinload(DoctorOrm.specialities)
        )
        result = await self.session.execute(query)
        doctor = result.scalars().one_or_none()
        return doctor

    async def get_all_doctors(self) -> List[DoctorOrm]:
        query = select(DoctorOrm).options(
            sqlalchemy.orm.selectinload(DoctorOrm.specialities)
        )
        result = await self.session.execute(query)
        doctors = result.scalars().all()
        return doctors

    async def restore_doctor(self, doctor_id: int) -> None:
        stmt = update(DoctorOrm).where(DoctorOrm.id == doctor_id).values(deleted=False)
        await self.session.execute(stmt)
        await self.session.commit() 

    async def get_doctors_by_speciality(self, speciality_id: int) -> List[DoctorOrm]:
        query = select(DoctorOrm).join(
            doctor_specialities,
            DoctorOrm.id == doctor_specialities.c.doctor_id
        ).where(
            doctor_specialities.c.speciality_id == speciality_id
        ).options(
            sqlalchemy.orm.selectinload(DoctorOrm.specialities)
        )
        result = await self.session.execute(query)
        doctors = result.scalars().all()
        return doctors 