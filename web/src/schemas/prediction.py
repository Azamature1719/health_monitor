from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List
from src.schemas.result import ResultRead 

class AnalyticsRequest(BaseModel):
    patient_id: int
    results: List[ResultRead]

class HypertensionPrediction(BaseModel):
    patient_id: int
    probability: float = Field(..., ge=0, le=1)
    predicted_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat()
        }

class AnalyticsResponse(BaseModel):
    success: bool
    message: str
    data: HypertensionPrediction | None = None