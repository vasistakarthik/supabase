
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class TokenManager:

    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, user_id: str) -> str:

        if not self.secret_key or len(self.secret_key) < 32:
            raise ValueError("JWT secret must contain at least 32 characters")

        now = datetime.now(timezone.utc)

        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + timedelta(minutes=self.expire_minutes)
        }

        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )
        logger.info("JWT access token generated successfully!")
        return token

    def verify_access_token(self, token: str) -> dict | None:

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            return payload

        except InvalidTokenError:
            return None


token_manager = TokenManager()
