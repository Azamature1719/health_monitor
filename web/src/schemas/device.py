# src/schemas/device.py
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class DeviceRegistrationRequest(BaseModel):
    device_id: UUID
    device_model: str = Field(..., min_length=1, max_length=100)
    device_type: str = Field(..., min_length=1, max_length=50)

class DeviceActivationRequest(BaseModel):
    activation_code: str = Field(..., min_length=6, max_length=6)
    patient_id: int

class DeviceAuthRequest(BaseModel):
    device_id: UUID
    access_token: str

class DeviceResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None

    class Config:
        from_attributes = True