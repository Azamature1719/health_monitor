from typing import List
import httpx
from src.core.config import settings
from src.schemas.prediction import AnalyticsRequest, AnalyticsResponse
from src.schemas.result import ResultRead

class AnalyticsClient:
    def __init__(self):
        self.base_url = settings.ANALYTICS_SERVICE_URL
        self.api_key = settings.ANALYTICS_API_KEY

    async def get_prediction(
        self,
        patient_id: int,
        results: List[ResultRead]
    ) -> AnalyticsResponse:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/predict",
                headers={
                    "X-API-Key": self.api_key,
                    "Content-Type": "application/json"
                },
                json=AnalyticsRequest(
                    patient_id=patient_id,
                    results=results
                ).model_dump()
            )
            response.raise_for_status()
            return AnalyticsResponse(**response.json())