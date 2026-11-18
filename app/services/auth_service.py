
from fastapi import HTTPException, status

from app.repositories.user_repository import user_repository
from app.utils.password_utils import password_manager
from app.utils.token_utils import token_manager
from app.schemas.auth import LoginRequest


class AuthService:

    def __init__(self):
        self.repository = user_repository

    def login(self, login_data: LoginRequest):

        user = self.repository.get_user_by_email(
            login_data.email
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        is_password_valid = password_manager.verify_password(
            login_data.password,
            user["hashed_password"]
        )

        if not is_password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = token_manager.create_access_token(
            str(user["id"])
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


auth_service = AuthService()
