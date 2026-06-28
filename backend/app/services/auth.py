from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    normalize_phone,
    verify_password,
)
from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.models.user import User
from app.repositories.auth import AuthRepository
from app.schemas.auth import RegisterRequest


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = AuthRepository(db)

    def register(self, req: RegisterRequest) -> tuple[User, str, str]:
        phone = normalize_phone(req.phone)

        if self.repo.get_by_phone(phone):
            raise AppError("phone_conflict", "Phone number already registered", 409)

        if req.farmer_status == FarmerStatus.owner:
            org = self.repo.create_organization(name=req.name)
            organization_id = org.id
            primary_farm_id = None
            membership_status = MembershipStatus.active
            account_status = AccountStatus.active_pending_verification
        else:
            if not req.farm_id:
                raise AppError("farm_id_required", "farm_id is required for owner_family and farm_staff", 422)
            farm = self.repo.get_farm_by_id(req.farm_id)
            if not farm:
                raise AppError("farm_not_found", "Farm not found", 404)
            organization_id = farm.organization_id
            primary_farm_id = farm.id
            membership_status = MembershipStatus.pending_farm_approval
            account_status = AccountStatus.active

        user = self.repo.create_user(
            id=uuid4(),
            organization_id=organization_id,
            name=req.name,
            phone=phone,
            password_hash=hash_password(req.password),
            role=UserRole.farmer,
            farmer_status=req.farmer_status,
            membership_status=membership_status,
            account_status=account_status,
            primary_farm_id=primary_farm_id,
            registered_at=datetime.now(timezone.utc),
        )

        self.db.commit()

        access_token = create_access_token(
            str(user.id), str(organization_id), UserRole.farmer.value
        )
        refresh_token = create_refresh_token(str(user.id))
        return user, access_token, refresh_token

    def login(self, phone: str, password: str) -> tuple[str, str]:
        normalized = normalize_phone(phone)
        user = self.repo.get_by_phone(normalized)
        if not user or not user.password_hash or not verify_password(password, user.password_hash):
            raise AppError("invalid_credentials", "Invalid phone or password", 401)

        role = user.role.value if user.role else UserRole.farmer.value
        access_token = create_access_token(str(user.id), str(user.organization_id), role)
        refresh_token = create_refresh_token(str(user.id))
        return access_token, refresh_token

    def refresh(self, refresh_token: str) -> str:
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise AppError("invalid_token", "Invalid or expired refresh token", 401)

        if payload.get("type") != "refresh":
            raise AppError("invalid_token", "Invalid token type", 401)

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise AppError("invalid_token", "Missing subject in token", 401)

        user = self.repo.get_by_id(UUID(user_id_str))
        if not user:
            raise AppError("user_not_found", "User not found", 401)

        role = user.role.value if user.role else UserRole.farmer.value
        return create_access_token(str(user.id), str(user.organization_id), role)

    def get_user_by_id(self, user_id: UUID) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise AppError("user_not_found", "User not found", 401)
        return user
