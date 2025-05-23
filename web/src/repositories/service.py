from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete
from src.models import ServiceOrm
from typing import List

class ServiceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_service(self, name: str) -> int:
        service = ServiceOrm(name=name)
        self.session.add(service)
        await self.session.flush()
        await self.session.commit()
        return service.id

    async def update_service(self, service_id: int, name: str):
        stmt = update(ServiceOrm).where(ServiceOrm.id == service_id).values(name=name)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_service(self, service_id: int):
        stmt = delete(ServiceOrm).where(ServiceOrm.id == service_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_service_by_id(self, service_id: int) -> ServiceOrm:
        query = select(ServiceOrm).where(ServiceOrm.id == service_id)
        result = await self.session.execute(query)
        service = result.scalars().one_or_none()
        return service

    async def get_all_services(self) -> List[ServiceOrm]:
        query = select(ServiceOrm)
        result = await self.session.execute(query)
        services = result.scalars().all()
        return services 