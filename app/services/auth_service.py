
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import user_repository
from app.utils.password_utils import password_manager
from app.utils.token_utils import token_manager

from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:

    def __init__(self):
        self.repository = user_repository

    # User registration
    def register(
        self,
        db: Session,
        register_data: RegisterRequest
    ):

        # Check whether email already exists
        existing_user = self.repository.get_user_by_email(
            db,
            register_data.email
        )

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = password_manager.hash_password(
            register_data.password
        )

        # Prepare user data
        user_data = {
            "email": str(register_data.email),
            "hashed_password": hashed_password,
            "is_active": True
        }

        # Save user in PostgreSQL
        user = self.repository.create_user(
            db,
            user_data
        )

        return user

    # User login
    def login(
        self,
        db: Session,
        login_data: LoginRequest
    ):

        user = self.repository.get_user_by_email(
            db,
            login_data.email
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        is_password_valid = password_manager.verify_password(
            login_data.password,
            user.hashed_password
        )

        if not is_password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = token_manager.create_access_token(
            str(user.id)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


auth_service = AuthService()
