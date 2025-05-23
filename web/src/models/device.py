# src/models/device.py
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, TIMESTAMP
from src.database import Model

class DeviceRegistrationOrm(Model):
    __tablename__ = "device_registrations"

    device_id: Mapped[UUID] = mapped_column(primary_key=True)
    device_model: Mapped[str]
    device_type: Mapped[str]
    activation_code: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    status: Mapped[str]  # pending, activated, expired

class DeviceActivationOrm(Model):
    __tablename__ = "device_activations"

    device_id: Mapped[UUID] = mapped_column(ForeignKey("device_registrations.device_id"), primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    activated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    access_token: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

class AuthSessionOrm(Model):
    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[UUID] = mapped_column(ForeignKey("device_registrations.device_id"))
    access_token: Mapped[str]
    last_login: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    token_expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    is_valid: Mapped[bool] = mapped_column(default=True)
    