from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories import PatientRepository
from src.database import get_db_session
from typing import List
from src.schemas import PatientCreate, PatientRead
from datetime import datetime

router = APIRouter(prefix="/patients", tags=["Patients"])

def get_patient_repository(session: AsyncSession = Depends(get_db_session)) -> PatientRepository:
    return PatientRepository(session=session)

@router.post("/", response_model=PatientRead)
async def create_patient(
    lastName: str = Form(...),
    firstName: str = Form(...),
    middleName: str = Form(...),
    birthDate: str = Form(...),
    city: str = Form(...),
    additionalInfo: str = Form(None),
    repo: PatientRepository = Depends(get_patient_repository)
):
    try:
        # Convert birthDate from string to date
        birth_date_obj = datetime.strptime(birthDate, "%d-%m-%Y").date()
        patient_id = await repo.add_patient(lastName, firstName, middleName, birth_date_obj, city, additionalInfo)
        return PatientRead(id=patient_id, lastName=lastName, firstName=firstName, middleName=middleName, birthDate=birth_date_obj, city=city, additionalInfo=additionalInfo, deleted=False)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create patient: {str(e)}")

@router.put("/{patient_id}", response_model=PatientRead)
async def update_patient(
    patient_id: int,
    lastName: str = Form(None),
    firstName: str = Form(None),
    middleName: str = Form(None),
    birthDate: str = Form(None),
    city: str = Form(None),
    additionalInfo: str = Form(None),
    repo: PatientRepository = Depends(get_patient_repository)
):
    try:
        birth_date_obj = datetime.strptime(birthDate, "%d-%m-%Y").date() if birthDate else None
        await repo.update_patient(patient_id, lastName, firstName, middleName, birth_date_obj, city, additionalInfo)
   
        updated_patient = await repo.get_patient_by_id(patient_id)
        return PatientRead.from_orm(updated_patient)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update patient: {str(e)}")

@router.delete("/{patient_id}")
async def delete_patient(patient_id: int, repo: PatientRepository = Depends(get_patient_repository)):
    try:
        await repo.mark_patient_deleted(patient_id)
        return {"message": "Patient marked as deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to mark patient as deleted: {str(e)}")

@router.put("/{patient_id}/restore")
async def restore_patient(patient_id: int, repo: PatientRepository = Depends(get_patient_repository)):
    try:
        await repo.restore_patient(patient_id)
        return {"message": "Patient restored successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to restore patient: {str(e)}")

@router.get("/{patient_id}", response_model=PatientRead)
async def get_patient(patient_id: int, repo: PatientRepository = Depends(get_patient_repository)):
    try:
        patient = await repo.get_patient_by_id(patient_id)
        if patient is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        return PatientRead.from_orm(patient)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get patient: {str(e)}")

@router.get("/", response_model=List[PatientRead])
async def get_all_patients(repo: PatientRepository = Depends(get_patient_repository)):
    try:
        patients = await repo.get_all_patients()
        return [PatientRead.from_orm(patient) for patient in patients]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get patients: {str(e)}") 