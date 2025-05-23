from fastapi import APIRouter, HTTPException, Depends, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories import DoctorRepository
from src.database import get_db_session
from typing import List, Optional
from src.schemas import DoctorCreate, DoctorRead

router = APIRouter(prefix="/doctors", tags=["Doctors"])

def get_doctor_repository(session: AsyncSession = Depends(get_db_session)) -> DoctorRepository:
    return DoctorRepository(session=session)

@router.post("/", response_model=DoctorRead)
async def create_doctor(
    lastName: str = Form(...),
    firstName: str = Form(...),
    middleName: str = Form(...),
    workplace: str = Form(...),
    speciality_ids: Optional[List[int]] = Query(None),
    repo: DoctorRepository = Depends(get_doctor_repository)
):
    try:
        doctor_id = await repo.add_doctor(lastName, firstName, middleName, workplace, speciality_ids)
        # Получаем созданного врача для возврата в ответе
        doctor = await repo.get_doctor_by_id(doctor_id)
        return DoctorRead.from_orm(doctor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create doctor: {str(e)}")

@router.put("/{doctor_id}", response_model=DoctorRead)
async def update_doctor(
    doctor_id: int,
    lastName: str = Form(None),
    firstName: str = Form(None),
    middleName: str = Form(None),
    workplace: str = Form(None),
    speciality_ids: Optional[List[int]] = Query(None),
    repo: DoctorRepository = Depends(get_doctor_repository)
):
    try:
        await repo.update_doctor(doctor_id, lastName, firstName, middleName, workplace, speciality_ids)
        doctor = await repo.get_doctor_by_id(doctor_id)
        return DoctorRead.from_orm(doctor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update doctor: {str(e)}")

@router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: int, repo: DoctorRepository = Depends(get_doctor_repository)):
    try:
        await repo.mark_doctor_deleted(doctor_id)
        return {"message": "Doctor marked as deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to mark doctor as deleted: {str(e)}")

@router.get("/{doctor_id}", response_model=DoctorRead)
async def get_doctor(doctor_id: int, repo: DoctorRepository = Depends(get_doctor_repository)):
    try:
        doctor = await repo.get_doctor_by_id(doctor_id)
        if doctor is None:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return DoctorRead.from_orm(doctor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get doctor: {str(e)}")

@router.get("/", response_model=List[DoctorRead])
async def get_all_doctors(repo: DoctorRepository = Depends(get_doctor_repository)):
    try:
        doctors = await repo.get_all_doctors()
        return [DoctorRead.from_orm(doctor) for doctor in doctors]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get doctors: {str(e)}")

@router.put("/{doctor_id}/restore")
async def restore_doctor(doctor_id: int, repo: DoctorRepository = Depends(get_doctor_repository)):
    try:
        await repo.restore_doctor(doctor_id)
        return {"message": "Doctor restored successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to restore doctor: {str(e)}")

@router.post("/{doctor_id}/specialities", response_model=DoctorRead)
async def set_doctor_specialities(
    doctor_id: int,
    speciality_ids: List[int],
    repo: DoctorRepository = Depends(get_doctor_repository)
):
    try:
        doctor = await repo.get_doctor_by_id(doctor_id)
        if doctor is None:
            raise HTTPException(status_code=404, detail="Doctor not found")
            
        await repo.update_doctor(doctor_id, speciality_ids=speciality_ids)
        updated_doctor = await repo.get_doctor_by_id(doctor_id)
        return DoctorRead.from_orm(updated_doctor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to set doctor specialities: {str(e)}")

@router.get("/by-speciality/{speciality_id}", response_model=List[DoctorRead])
async def get_doctors_by_speciality(speciality_id: int, repo: DoctorRepository = Depends(get_doctor_repository)):
    try:
        doctors = await repo.get_doctors_by_speciality(speciality_id)
        return [DoctorRead.from_orm(doctor) for doctor in doctors]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get doctors by speciality: {str(e)}") 