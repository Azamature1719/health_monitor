from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import OrderCreate, OrderRead, PatientRead, SimpleDoctorRead
from src.repositories import OrderRepository
from src.database import get_db_session

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_order_repository(session: AsyncSession = Depends(get_db_session)) -> OrderRepository:
    return OrderRepository(session=session)

@router.post("/", response_model=OrderRead) 
async def create_order(order_data: OrderCreate, repo: OrderRepository = Depends(get_order_repository)):
    try:
        order_id = await repo.add_one(order_data)

        return OrderRead(orderId=order_id, **order_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create order: {str(e)}")


@router.get("/{id}", response_model=OrderRead)
async def get_order(id: int, repo: OrderRepository = Depends(get_order_repository)):
    try:
        order_model = await repo.find_one(id)
        if order_model is None:
            raise HTTPException(status_code=404, detail=f"Order with id {id} not found")
        
        try:
            order_dict = {
                "orderId": order_model.orderId,
                "typeName": order_model.typeName,
                "title": order_model.title,
                "unit": order_model.unit,
                "startDate": order_model.startDate,
                "endDate": order_model.endDate,
                "executionTimes": order_model.executionTimes,
                "patientId": order_model.patientId,
                "description": order_model.description,
                "status": order_model.status,
                "doctorId": order_model.doctorId
            }
            
            response = OrderRead(**order_dict)
            
            if hasattr(order_model, "patient") and order_model.patient is not None:
                try:
                    response.patient = PatientRead.from_orm(order_model.patient)
                except Exception as patient_error:
                    print(f"Error loading patient for order {id}: {str(patient_error)}")
            
            if hasattr(order_model, "doctor") and order_model.doctor is not None:
                try:
                    response.doctor = SimpleDoctorRead.from_orm(order_model.doctor)
                except Exception as doctor_error:
                    print(f"Error loading doctor for order {id}: {str(doctor_error)}")
                    
            return response
            
        except Exception as model_error:
            raise HTTPException(status_code=500, detail=f"Error processing order data: {str(model_error)}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve order: {str(e)}")


@router.get("/", response_model=List[OrderRead])
async def get_all_orders(
    repo: OrderRepository = Depends(get_order_repository)
):
    try:
        order_models = await repo.find_all()
        result = []
        
        for order_model in order_models:
            try:
                order_dict = {
                    "orderId": order_model.orderId,
                    "typeName": order_model.typeName,
                    "title": order_model.title,
                    "unit": order_model.unit,
                    "startDate": order_model.startDate,
                    "endDate": order_model.endDate,
                    "executionTimes": order_model.executionTimes,
                    "patientId": order_model.patientId,
                    "description": order_model.description,
                    "status": order_model.status,
                    "doctorId": order_model.doctorId
                }
            
                # Создаем объект ответа
                order_read = OrderRead(**order_dict)
                
                if hasattr(order_model, "patient") and order_model.patient is not None:
                    try:
                        order_read.patient = PatientRead.from_orm(order_model.patient)
                    except Exception as patient_error:
                        print(f"Error loading patient for order {order_model.orderId}: {str(patient_error)}")
                
                if hasattr(order_model, "doctor") and order_model.doctor is not None:
                    try:
                        order_read.doctor = SimpleDoctorRead.from_orm(order_model.doctor)
                    except Exception as doctor_error:
                        print(f"Error loading doctor for order {order_model.orderId}: {str(doctor_error)}")
                    
                result.append(order_read)
            except Exception as model_error:
                print(f"Error processing order {getattr(order_model, 'orderId', 'unknown')}: {str(model_error)}")
                continue
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve orders: {str(e)}")

@router.get("/by-patient/{patient_id}", response_model=List[OrderRead])
async def get_orders_by_patient(
    patient_id: int,
    repo: OrderRepository = Depends(get_order_repository)
):
    try:
        order_models = await repo.find_by_patient(patient_id)
        result = []
        
        for order_model in order_models:
            try:
                order_dict = {
                    "orderId": order_model.orderId,
                    "typeName": order_model.typeName,
                    "title": order_model.title,
                    "unit": order_model.unit,
                    "startDate": order_model.startDate,
                    "endDate": order_model.endDate,
                    "executionTimes": order_model.executionTimes,
                    "patientId": order_model.patientId,
                    "description": order_model.description,
                    "status": order_model.status,
                    "doctorId": order_model.doctorId
                }
    
                order_read = OrderRead(**order_dict)
                
                if hasattr(order_model, "doctor") and order_model.doctor is not None:
                    try:
                        order_read.doctor = SimpleDoctorRead.from_orm(order_model.doctor)
                    except Exception as doctor_error:
                        print(f"Error loading doctor for order {order_model.orderId}: {str(doctor_error)}")
                    
                result.append(order_read)
            except Exception as model_error:
                print(f"Error processing order {getattr(order_model, 'orderId', 'unknown')}: {str(model_error)}")
                continue
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve orders for patient {patient_id}: {str(e)}")

@router.get("/by-doctor/{doctor_id}", response_model=List[OrderRead])
async def get_orders_by_doctor(
    doctor_id: int,
    repo: OrderRepository = Depends(get_order_repository)
):
    try:
        order_models = await repo.find_by_doctor(doctor_id)
        result = []
        
        for order_model in order_models:
            try:
                order_dict = {
                    "orderId": order_model.orderId,
                    "typeName": order_model.typeName,
                    "title": order_model.title,
                    "unit": order_model.unit,
                    "startDate": order_model.startDate,
                    "endDate": order_model.endDate,
                    "executionTimes": order_model.executionTimes,
                    "patientId": order_model.patientId,
                    "description": order_model.description,
                    "status": order_model.status,
                    "doctorId": order_model.doctorId
                }
                
                order_read = OrderRead(**order_dict)
                
                if hasattr(order_model, "patient") and order_model.patient is not None:
                    try:
                        order_read.patient = PatientRead.from_orm(order_model.patient)
                    except Exception as patient_error:
                        print(f"Error loading patient for order {order_model.orderId}: {str(patient_error)}")
                    
                result.append(order_read)
            except Exception as model_error:
                print(f"Error processing order {getattr(order_model, 'orderId', 'unknown')}: {str(model_error)}")
                continue
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve orders for doctor {doctor_id}: {str(e)}") 