from datetime import datetime, timedelta, timezone
import random
import jwt
from uuid import UUID
from src.core.config import settings

class TokenService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.activation_code_ttl = settings.ACTIVATION_CODE_TTL  
        self.token_ttl = settings.TOKEN_TTL 

    def generate_activation_code(self) -> tuple[str, datetime]:
        code = ''.join(random.choices('0123456789', k=6))
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.activation_code_ttl)
        return code, expires_at

    def generate_access_token(self, device_id: UUID, patient_id: int) -> tuple[str, datetime]:
        expires_at = datetime.now(timezone.utc) + timedelta(days=self.token_ttl)
        payload = {
            'device_id': str(device_id),
            'patient_id': patient_id,
            'exp': expires_at.timestamp()
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token, expires_at

    def verify_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None