from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from src.database import get_db_session
from src.services.analytics_client import AnalyticsClient
from src.repositories.prediction import PredictionRepository
from src.repositories.result import ResultRepository
from src.schemas.prediction import AnalyticsResponse, HypertensionPrediction

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])
analytics_client = AnalyticsClient()

@router.post("/{patient_id}", response_model=AnalyticsResponse)
async def predict_hypertension(
    patient_id: int,
    days: int = 1,
    db: AsyncSession = Depends(get_db_session)
) -> AnalyticsResponse:
    """
    Получает прогноз вероятности гипертензии на основе результатов измерений
    за указанное количество дней
    """
    # Получаем результаты измерений
    result_repository = ResultRepository(db)
    from_date = datetime.now(timezone.utc) - timedelta(days=days)
    results = await result_repository.get_patient_results(
        patient_id=patient_id,
        from_date=from_date
    )
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail="No results found for the specified period"
        )

    # Получаем прогноз
    try:
        prediction = await analytics_client.get_prediction(
            patient_id=patient_id,
            results=results
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Analytics service error: {str(e)}"
        )

    # Сохраняем результат
    prediction_repository = PredictionRepository(db)
    await prediction_repository.create_prediction(
        patient_id=patient_id,
        probability=prediction.data.probability
    )

    return prediction

@router.get("/{patient_id}/latest", response_model=AnalyticsResponse)
async def get_latest_prediction(
    patient_id: int,
    db: AsyncSession = Depends(get_db_session)
) -> AnalyticsResponse:
    """
    Получает последний прогноз для пациента
    """
    repository = PredictionRepository(db)
    prediction = await repository.get_latest_prediction(patient_id)
    
    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="No predictions found for this patient"
        )

    return AnalyticsResponse(
        success=True,
        message="Latest prediction retrieved",
        data=HypertensionPrediction(
            patient_id=prediction.patient_id,
            probability=prediction.probability,
            predicted_at=prediction.predicted_at
        )
    )