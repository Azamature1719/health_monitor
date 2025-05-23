from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db_session
from src.schemas.device import (
    DeviceRegistrationRequest,
    DeviceActivationRequest,
    DeviceAuthRequest,
    DeviceResponse
)
from src.services.token_service import TokenService
from src.repositories.device import DeviceRepository

router = APIRouter(prefix="/api/devices", tags=["Devices"])
token_service = TokenService()

@router.post("/register", response_model=DeviceResponse)
async def register_device(
    request: DeviceRegistrationRequest,
    db: AsyncSession = Depends(get_db_session)
) -> DeviceResponse:
    repository = DeviceRepository(db)
    
    activation_code, expires_at = token_service.generate_activation_code()
    
    await repository.create_registration(
        device_id=request.device_id,
        device_model=request.device_model,
        device_type=request.device_type,
        activation_code=activation_code,
        expires_at=expires_at
    )
    
    return DeviceResponse(
        success=True,
        message="Device registered successfully",
        data={
            "activation_code": activation_code,
            "expires_in": token_service.activation_code_ttl
        }
    )

@router.post("/activate", response_model=DeviceResponse)
async def activate_device(
    request: DeviceActivationRequest,
    db: AsyncSession = Depends(get_db_session)
) -> DeviceResponse:
    repository = DeviceRepository(db)
    
    registration = await repository.get_registration_by_code(request.activation_code)
    if not registration:
        raise HTTPException(status_code=400, detail="Invalid or expired activation code")

    access_token, expires_at = token_service.generate_access_token(
        registration.device_id, request.patient_id
    )

    await repository.create_activation(
        device_id=registration.device_id,
        patient_id=request.patient_id,
        access_token=access_token
    )

    return DeviceResponse(
        success=True,
        message="Device activated successfully",
        data={
            "access_token": access_token,
            "expires_in": token_service.token_ttl * 24 * 3600
        }
    )

@router.get("/{device_id}/status", response_model=DeviceResponse)
async def check_activation_status(
    device_id: UUID,
    db: AsyncSession = Depends(get_db_session)
) -> DeviceResponse:
    repository = DeviceRepository(db)
    
    activation = await repository.get_activation(device_id)
    if not activation:
        return DeviceResponse(
            success=True,
            message="Device not activated",
            data={
                "is_activated": False,
                "status": "pending"
            }
        )

    return DeviceResponse(
        success=True,
        message="Device status retrieved",
        data={
            "is_activated": True,
            "status": "activated",
            "access_token": activation.access_token
        }
    )

@router.post("/auth/login", response_model=DeviceResponse)
async def login(
    request: DeviceAuthRequest,
    db: AsyncSession = Depends(get_db_session)
) -> DeviceResponse:
    repository = DeviceRepository(db)
    
    payload = token_service.verify_token(request.access_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    activation = await repository.get_activation(request.device_id)
    if not activation:
        raise HTTPException(status_code=401, detail="Device not activated")

    new_token, expires_at = token_service.generate_access_token(
        request.device_id, 
        payload['patient_id']
    )

    await repository.create_auth_session(
        device_id=request.device_id,
        access_token=new_token,
        expires_at=expires_at
    )

    return DeviceResponse(
        success=True,
        message="Authentication successful",
        data={
            "access_token": new_token,
            "expires_in": token_service.token_ttl * 24 * 3600,
            "token_type": "Bearer"
        }
    )