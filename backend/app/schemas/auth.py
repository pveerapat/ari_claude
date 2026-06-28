from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus


class RegisterRequest(BaseModel):
    phone: str
    name: str
    password: str
    farmer_status: FarmerStatus
    farm_id: Optional[UUID] = None


class LoginRequest(BaseModel):
    phone: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RegisterResponse(BaseModel):
    user_id: UUID
    phone: str
    role: str
    farmer_status: FarmerStatus
    organization_id: UUID
    account_status: Optional[AccountStatus] = None
    membership_status: Optional[MembershipStatus] = None
    primary_farm_id: Optional[UUID] = None
    access_token: str
    refresh_token: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class MeResponse(BaseModel):
    user_id: UUID
    phone: Optional[str] = None
    name: str
    role: Optional[str] = None
    farmer_status: Optional[FarmerStatus] = None
    organization_id: UUID
    primary_farm_id: Optional[UUID] = None
    membership_status: Optional[MembershipStatus] = None
    account_status: Optional[AccountStatus] = None


class LogoutResponse(BaseModel):
    success: bool = True
