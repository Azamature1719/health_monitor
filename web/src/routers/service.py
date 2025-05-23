from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories import ServiceRepository
from src.database import get_db_session
from typing import List
from src.schemas import ServiceCreate, ServiceRead

router = APIRouter(prefix="/services", tags=["Services"])

def get_service_repository(session: AsyncSession = Depends(get_db_session)) -> ServiceRepository:
    return ServiceRepository(session=session)

@router.post("/", response_model=ServiceRead)
async def create_service(name: str = Form(...), repo: ServiceRepository = Depends(get_service_repository)):
    try:
        service_id = await repo.add_service(name)
        return ServiceRead(id=service_id, name=name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create service: {str(e)}")

@router.put("/{service_id}", response_model=ServiceRead)
async def update_service(service_id: int, name: str = Form(...), repo: ServiceRepository = Depends(get_service_repository)):
    try:
        await repo.update_service(service_id, name)
        updated_service = await repo.get_service_by_id(service_id)
        return ServiceRead.from_orm(updated_service)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update service: {str(e)}")

@router.delete("/{service_id}")
async def delete_service(service_id: int, repo: ServiceRepository = Depends(get_service_repository)):
    try:
        await repo.delete_service(service_id)
        return {"message": "Service deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete service: {str(e)}")

@router.get("/{service_id}", response_model=ServiceRead)
async def get_service(service_id: int, repo: ServiceRepository = Depends(get_service_repository)):
    try:
        service = await repo.get_service_by_id(service_id)
        if service is None:
            raise HTTPException(status_code=404, detail="Service not found")
        return ServiceRead.from_orm(service)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get service: {str(e)}")

@router.get("/", response_model=List[ServiceRead])
async def get_all_services(repo: ServiceRepository = Depends(get_service_repository)):
    try:
        services = await repo.get_all_services()
        return [ServiceRead.from_orm(service) for service in services]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get services: {str(e)}") 