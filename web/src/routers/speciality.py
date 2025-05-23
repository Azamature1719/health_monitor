from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories import SpecialityRepository
from src.database import get_db_session
from typing import List
from src.schemas import SpecialityCreate, SpecialityRead

router = APIRouter(prefix="/specialities", tags=["Specialities"])

def get_speciality_repository(session: AsyncSession = Depends(get_db_session)) -> SpecialityRepository:
    return SpecialityRepository(session=session)

@router.post("/", response_model=SpecialityRead)
async def create_speciality(name: str = Form(...), repo: SpecialityRepository = Depends(get_speciality_repository)):
    try:
        existing_speciality = await repo.get_speciality_by_name(name)
        if existing_speciality:
            raise HTTPException(status_code=400, detail="Специализация с таким названием уже создана")
        
        speciality_id = await repo.add_speciality(name)
        return SpecialityRead(id=speciality_id, name=name)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create speciality: {str(e)}")

@router.put("/{speciality_id}", response_model=SpecialityRead)
async def update_speciality(speciality_id: int, name: str = Form(...), repo: SpecialityRepository = Depends(get_speciality_repository)):
    try:
        await repo.update_speciality(speciality_id, name)
        updated_speciality = await repo.get_speciality_by_id(speciality_id)
        return SpecialityRead.from_orm(updated_speciality)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update speciality: {str(e)}")

@router.delete("/{speciality_id}")
async def delete_speciality(speciality_id: int, repo: SpecialityRepository = Depends(get_speciality_repository)):
    try:
        await repo.delete_speciality(speciality_id)
        return {"message": "Speciality deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete speciality: {str(e)}")

@router.get("/{speciality_id}", response_model=SpecialityRead)
async def get_speciality(speciality_id: int, repo: SpecialityRepository = Depends(get_speciality_repository)):
    try:
        speciality = await repo.get_speciality_by_id(speciality_id)
        if speciality is None:
            raise HTTPException(status_code=404, detail="Speciality not found")
        return SpecialityRead.from_orm(speciality)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get speciality: {str(e)}")

@router.get("/", response_model=List[SpecialityRead])
async def get_all_specialities(repo: SpecialityRepository = Depends(get_speciality_repository)):
    try:
        specialities = await repo.get_all_specialities()
        return [SpecialityRead.from_orm(speciality) for speciality in specialities]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get specialities: {str(e)}") 