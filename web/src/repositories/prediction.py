from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.prediction import PredictionOrm

class PredictionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_prediction(
        self,
        patient_id: int,
        probability: float
    ) -> PredictionOrm:
        prediction = PredictionOrm(
            patient_id=patient_id,
            probability=probability
        )
        self.session.add(prediction)
        await self.session.commit()
        return prediction

    async def get_latest_prediction(
        self,
        patient_id: int
    ) -> PredictionOrm | None:
        query = select(PredictionOrm).where(
            PredictionOrm.patient_id == patient_id
        ).order_by(PredictionOrm.predicted_at.desc())
        result = await self.session.execute(query)
        return result.scalar_one_or_none()