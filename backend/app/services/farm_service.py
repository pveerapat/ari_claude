from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.models.farm import Farm
from app.models.user import User
from app.repositories.farms import FarmRepository
from app.schemas.farm import FarmCreate, FarmUpdate
from app.services.base import BaseService
from app.utils.pagination import calc_offset, clamp_page, clamp_page_size


_PRIVILEGED_ROLES = {UserRole.admin, UserRole.root, UserRole.ari_staff}


def _is_privileged(user: User) -> bool:
    return user.role in _PRIVILEGED_ROLES


def _assert_active_membership(user: User) -> None:
    if user.membership_status != MembershipStatus.active:
        raise AppError("membership_not_active", "Farm membership is not active", 403)


def _assert_owner_write(user: User) -> None:
    if _is_privileged(user):
        return
    if user.farmer_status != FarmerStatus.owner:
        raise AppError("farm_create_forbidden", "Only farm owners can perform this action", 403)
    _assert_active_membership(user)


def _assert_org_scope(user: User, organization_id: UUID) -> None:
    if _is_privileged(user):
        return
    if user.organization_id != organization_id:
        raise AppError("organization_not_accessible", "Organization is not accessible", 403)


class FarmService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = FarmRepository(db)

    def list_farms(
        self,
        user: User,
        organization_id: UUID | None = None,
        status: str | None = None,
        q: str | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Farm], int]:
        page = clamp_page(page)
        page_size = clamp_page_size(page_size)
        offset = calc_offset(page, page_size)

        if _is_privileged(user):
            scope_org_id = organization_id or user.organization_id
        else:
            scope_org_id = user.organization_id
            if organization_id and organization_id != scope_org_id:
                raise AppError("organization_not_accessible", "Organization is not accessible", 403)

        farms = self.repo.list_by_org(scope_org_id, status, q, offset, page_size, sort_by, sort_order)
        total = self.repo.count_by_org(scope_org_id, status, q)
        return farms, total

    def get_farm(self, user: User, farm_id: UUID) -> Farm:
        farm = self.repo.get_by_id(farm_id)
        if not farm:
            raise AppError("farm_not_found", "Farm not found", 404)
        _assert_org_scope(user, farm.organization_id)
        return farm

    def create_farm(self, user: User, req: FarmCreate) -> Farm:
        _assert_owner_write(user)
        location = req.location.model_dump() if req.location else None
        farm = self.repo.create(
            organization_id=user.organization_id,
            name=req.farm_name,
            location=location,
            description=req.description,
        )
        self.db.commit()
        self.db.refresh(farm)
        return farm

    def update_farm(self, user: User, farm_id: UUID, req: FarmUpdate) -> Farm:
        farm = self.repo.get_by_id(farm_id)
        if not farm:
            raise AppError("farm_not_found", "Farm not found", 404)
        _assert_org_scope(user, farm.organization_id)
        if not _is_privileged(user):
            if user.farmer_status != FarmerStatus.owner:
                raise AppError("farm_create_forbidden", "Only farm owners can update farms", 403)

        updates: dict = {}
        if "farm_name" in req.model_fields_set and req.farm_name is not None:
            updates["name"] = req.farm_name
        if "location" in req.model_fields_set:
            updates["location"] = req.location.model_dump() if req.location else None
        if "description" in req.model_fields_set:
            updates["description"] = req.description

        if updates:
            farm = self.repo.update(farm, updates)
        self.db.commit()
        self.db.refresh(farm)
        return farm
