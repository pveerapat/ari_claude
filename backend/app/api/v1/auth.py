from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.response import success_response
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    svc = AuthService(db)
    user, access_token, refresh_token = svc.register(req)

    data: dict = {
        "user_id": str(user.id),
        "phone": user.phone,
        "role": user.role.value if user.role else "farmer",
        "farmer_status": user.farmer_status.value if user.farmer_status else None,
        "organization_id": str(user.organization_id),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    if user.account_status is not None:
        data["account_status"] = user.account_status.value
    if user.membership_status is not None:
        data["membership_status"] = user.membership_status.value
    if user.primary_farm_id is not None:
        data["primary_farm_id"] = str(user.primary_farm_id)

    return success_response(data)


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    svc = AuthService(db)
    access_token, refresh_token = svc.login(req.phone, req.password)
    return success_response({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    })


@router.post("/refresh")
def refresh(req: RefreshRequest, db: Session = Depends(get_db)):
    svc = AuthService(db)
    access_token = svc.refresh(req.refresh_token)
    return success_response({
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    })


@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return success_response({
        "user_id": str(user.id),
        "phone": user.phone,
        "name": user.name,
        "role": user.role.value if user.role else None,
        "farmer_status": user.farmer_status.value if user.farmer_status else None,
        "organization_id": str(user.organization_id),
        "primary_farm_id": str(user.primary_farm_id) if user.primary_farm_id else None,
        "membership_status": user.membership_status.value if user.membership_status else None,
        "account_status": user.account_status.value if user.account_status else None,
    })


@router.post("/logout")
def logout(_user: User = Depends(get_current_user)):
    return success_response({"success": True})
