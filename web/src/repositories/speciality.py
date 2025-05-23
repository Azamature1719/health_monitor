from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete
from src.models import SpecialityOrm
from typing import List

class SpecialityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_speciality(self, name: str) -> int:
        speciality = SpecialityOrm(name=name)
        self.session.add(speciality)
        await self.session.flush()
        await self.session.commit()
        return speciality.id

    async def update_speciality(self, speciality_id: int, name: str):
        stmt = update(SpecialityOrm).where(SpecialityOrm.id == speciality_id).values(name=name)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_speciality(self, speciality_id: int):
        stmt = delete(SpecialityOrm).where(SpecialityOrm.id == speciality_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_speciality_by_id(self, speciality_id: int) -> SpecialityOrm:
        query = select(SpecialityOrm).where(SpecialityOrm.id == speciality_id)
        result = await self.session.execute(query)
        speciality = result.scalars().one_or_none()
        return speciality

    async def get_all_specialities(self) -> List[SpecialityOrm]:
        query = select(SpecialityOrm)
        result = await self.session.execute(query)
        specialities = result.scalars().all()
        return specialities

    async def get_speciality_by_name(self, name: str) -> SpecialityOrm:
        query = select(SpecialityOrm).where(SpecialityOrm.name == name)
        result = await self.session.execute(query)
        speciality = result.scalars().one_or_none()
        return speciality 