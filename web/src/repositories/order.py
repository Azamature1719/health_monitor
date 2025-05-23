from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import sqlalchemy.orm

from src.models import OrderOrm 
from src.schemas import OrderCreate 

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: OrderCreate) -> int:
        order_dict = data.model_dump()
        order = OrderOrm(**order_dict)
        self.session.add(order)
        await self.session.flush()
        await self.session.commit()
        return order.orderId
    
    
    async def find_one(self, id: int) -> OrderOrm:
        try:
            query = select(OrderOrm).where(OrderOrm.orderId == id).options(
                sqlalchemy.orm.selectinload(OrderOrm.patient),
                sqlalchemy.orm.selectinload(OrderOrm.doctor)
            )
            result = await self.session.execute(query)
            one_order_model = result.scalars().one_or_none()
            return one_order_model          
        except Exception as e:
            raise Exception(status_code=404, detail=f"Order with id {id} not found")


    async def find_all(self) -> List[OrderOrm]:
        query = select(OrderOrm).options(
            sqlalchemy.orm.selectinload(OrderOrm.patient),
            sqlalchemy.orm.selectinload(OrderOrm.doctor)
        )
        result = await self.session.execute(query)
        order_models = result.scalars().all()
        return list(order_models)
        
    async def find_by_patient(self, patient_id: int) -> List[OrderOrm]:
        query = select(OrderOrm).where(OrderOrm.patientId == patient_id).options(
            sqlalchemy.orm.selectinload(OrderOrm.doctor)
        )
        result = await self.session.execute(query)
        order_models = result.scalars().all()
        return list(order_models)
        
    async def find_by_doctor(self, doctor_id: int) -> List[OrderOrm]:
        query = select(OrderOrm).where(OrderOrm.doctorId == doctor_id).options(
            sqlalchemy.orm.selectinload(OrderOrm.patient)
        )
        result = await self.session.execute(query)
        order_models = result.scalars().all()
        return list(order_models)