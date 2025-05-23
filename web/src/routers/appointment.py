from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories import AppointmentRepository
from src.database import get_db_session
from typing import List
from src.schemas import AppointmentCreate, AppointmentRead
from datetime import datetime

router = APIRouter(prefix="/appointments", tags=["Appointments"])

def get_appointment_repository(session: AsyncSession = Depends(get_db_session)) -> AppointmentRepository:
    return AppointmentRepository(session=session)

@router.post("/", response_model=AppointmentRead)
async def create_appointment(
    appointment_date: str = Form(...),
    appointment_time: str = Form(...),
    content: str = Form(None),
    doctor_id: int = Form(...),
    patient_id: int = Form(...),
    service_id: int = Form(...),
    status: str = Form(...),
    repo: AppointmentRepository = Depends(get_appointment_repository)
):
    try:
        # Преобразуем строки в объекты date и time
        date_obj = datetime.strptime(appointment_date, "%d-%m-%Y").date()
        time_obj = datetime.strptime(appointment_time, "%H:%M").time()
        
        appointment_id = await repo.add_appointment(
            date_obj, time_obj, content, doctor_id, patient_id, service_id, status
        )
        
        return AppointmentRead(
            id=appointment_id,
            appointment_date=date_obj,
            appointment_time=time_obj,
            content=content,
            doctor_id=doctor_id,
            patient_id=patient_id,
            service_id=service_id,
            status=status
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create appointment: {str(e)}")

@router.put("/{appointment_id}", response_model=AppointmentRead)
async def update_appointment(
    appointment_id: int,
    appointment_date: str = Form(None),
    appointment_time: str = Form(None),
    content: str = Form(None),
    doctor_id: int = Form(None),
    patient_id: int = Form(None),
    service_id: int = Form(None),
    status: str = Form(None),
    repo: AppointmentRepository = Depends(get_appointment_repository)
):
    try:
        # Преобразуем строки в объекты date и time, если они предоставлены
        date_obj = datetime.strptime(appointment_date, "%d-%m-%Y").date() if appointment_date else None
        time_obj = datetime.strptime(appointment_time, "%H:%M").time() if appointment_time else None
        
        await repo.update_appointment(
            appointment_id, date_obj, time_obj, content, doctor_id, patient_id, service_id, status
        )
        
        # Получаем обновленную запись
        updated_appointment = await repo.get_appointment_by_id(appointment_id)
        return AppointmentRead.from_orm(updated_appointment)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update appointment: {str(e)}")

@router.delete("/{appointment_id}")
async def delete_appointment(appointment_id: int, repo: AppointmentRepository = Depends(get_appointment_repository)):
    try:
        await repo.delete_appointment(appointment_id)
        return {"message": "Appointment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete appointment: {str(e)}")

@router.get("/{appointment_id}", response_model=AppointmentRead)
async def get_appointment(appointment_id: int, repo: AppointmentRepository = Depends(get_appointment_repository)):
    try:
        appointment = await repo.get_appointment_by_id(appointment_id)
        if appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return AppointmentRead.from_orm(appointment)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get appointment: {str(e)}")

@router.get("/", response_model=List[AppointmentRead])
async def get_all_appointments(repo: AppointmentRepository = Depends(get_appointment_repository)):
    try:
        appointments = await repo.get_all_appointments()
        return [AppointmentRead.from_orm(appointment) for appointment in appointments]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get appointments: {str(e)}")

@router.get("/doctor/{doctor_id}", response_model=List[AppointmentRead])
async def get_appointments_by_doctor(doctor_id: int, repo: AppointmentRepository = Depends(get_appointment_repository)):
    try:
        appointments = await repo.get_appointments_by_doctor(doctor_id)
        return [AppointmentRead.from_orm(appointment) for appointment in appointments]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get appointments by doctor: {str(e)}")

@router.get("/patient/{patient_id}", response_model=List[AppointmentRead])
async def get_appointments_by_patient(patient_id: int, repo: AppointmentRepository = Depends(get_appointment_repository)):
    try:
        appointments = await repo.get_appointments_by_patient(patient_id)
        return [AppointmentRead.from_orm(appointment) for appointment in appointments]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get appointments by patient: {str(e)}") 