from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import sys
import json

from src.schemas import ResultCreate, ResultRead
from src.repositories import ResultRepository
from src.database import get_db_session

router = APIRouter(prefix="/results", tags=["Results"])

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

async def get_result_repository(session: AsyncSession = Depends(get_db_session)) -> ResultRepository:
    return ResultRepository(session=session)

@router.post("/", response_model=ResultRead)
async def create_result(request: Request, result: ResultCreate, repo:ResultRepository = Depends(get_result_repository)) -> ResultRead:
    try:
        body = await request.json()
        logger.info(f"Received POST request with body: {json.dumps(body, default=str)}")
        
        logger.info(f"Validated data: {result.model_dump_json()}")
        
        result_id = await repo.add_one(result)
        return ResultRead(**result.model_dump(), id=result_id)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", response_model=ResultRead)
async def get_result(id: int, repo:ResultRepository = Depends(get_result_repository)) -> ResultRead:
    try:
        result_model = await repo.find_one(id)
        if result_model is None:
            raise HTTPException(status_code=404, detail=f"Result with id {id} not found")
        return ResultRead.model_validate(result_model.__dict__)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve result: {str(e)}")

@router.get("/", response_model=List[ResultRead])
async def get_all_results(repo:ResultRepository = Depends(get_result_repository)) -> List[ResultRead]:
    try:
        results_model = await repo.find_all()
        return [ResultRead.model_validate(result.__dict__) for result in results_model]
    except Exception as e:
        logger.error(f"Failed to retrieve results: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Failed to retrieve results: {str(e)}") 