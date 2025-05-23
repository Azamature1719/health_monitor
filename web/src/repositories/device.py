from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.device import DeviceRegistrationOrm, DeviceActivationOrm, AuthSessionOrm


class DeviceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_registration(
        self,
        device_id: UUID,
        device_model: str,
        device_type: str,
        activation_code: str,
        expires_at: datetime
    ) -> DeviceRegistrationOrm:
        registration = DeviceRegistrationOrm(
            device_id=device_id,
            device_model=device_model,
            device_type=device_type,
            activation_code=activation_code,
            expires_at=expires_at,
            status="pending"
        )
        self.session.add(registration)
        await self.session.commit()
        return registration

    async def get_registration_by_code(self, activation_code: str) -> DeviceRegistrationOrm | None:
        query = select(DeviceRegistrationOrm).where(
            DeviceRegistrationOrm.activation_code == activation_code,
            DeviceRegistrationOrm.expires_at > datetime.utcnow(),
            DeviceRegistrationOrm.status == "pending"
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_activation(self, device_id: UUID, patient_id: int,
                              access_token: str) -> DeviceActivationOrm:
        activation = DeviceActivationOrm(
            device_id=device_id,
            patient_id=patient_id,
            access_token=access_token,
            is_active=True
        )
        self.session.add(activation)
        await self.session.commit()
        return activation

    async def get_activation(self, device_id: UUID) -> DeviceActivationOrm | None:
        query = select(DeviceActivationOrm).where(
            DeviceActivationOrm.device_id == device_id,
            DeviceActivationOrm.is_active == True
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_auth_session(self, device_id: UUID, access_token: str,
                                expires_at: datetime) -> AuthSessionOrm:
        session = AuthSessionOrm(
            device_id=device_id,
            access_token=access_token,
            token_expires_at=expires_at,
            is_valid=True
        )
        self.session.add(session)
        await self.session.commit()
        return session