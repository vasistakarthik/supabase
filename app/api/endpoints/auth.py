
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse
)

from app.services.auth_service import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# User registration
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    return auth_service.register(db, register_data)


# User login
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    return auth_service.login(db, login_data)
