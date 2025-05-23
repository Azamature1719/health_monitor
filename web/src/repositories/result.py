from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.models import ResultOrm
from src.schemas import ResultCreate, ResultRead
from sqlalchemy import select


class ResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: ResultCreate) -> int:
        result_dict = data.model_dump()
        result = ResultOrm(**result_dict)
        self.session.add(result)
        await self.session.flush() 
        await self.session.commit()
        return result.id
    
    async def find_one(self, id: int) -> ResultOrm:
        query = select(ResultOrm).where(ResultOrm.id == id)
        result_model = await self.session.execute(query)
        one_result_model = result_model.scalars().one_or_none()
        return one_result_model
    
    async def find_all(self) -> List[ResultRead]:
        query = select(ResultOrm)
        result_model = await self.session.execute(query)
        result_scalars = result_model.scalars().all()
        results_schemas = [
            ResultRead(
                id=result.id, 
                resultIdMobile=result.resultIdMobile,
                title=result.title, 
                typeName=result.typeName,
                patientId=result.patientId,
                doctorId=result.doctorId,
                executionTime=result.executionTime,
                value=result.value,
                status=result.status,
                unit=result.unit, 
                orderId=result.orderId
                ) for result in result_scalars
            ]
        return results_schemas 