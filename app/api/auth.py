from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest
from app.core.config import settings
from app.core.security import create_access_token

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(data: LoginRequest):

    if (
        data.username != settings.ADMIN_USERNAME
        or data.password != settings.ADMIN_PASSWORD
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )

    token = create_access_token(
        {
            "sub": settings.ADMIN_USERNAME
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }