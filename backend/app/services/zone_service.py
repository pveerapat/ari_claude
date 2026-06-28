from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.models.user import User
from app.models.zone import Zone
from app.repositories.farms import FarmRepository
from app.repositories.zones import ZoneRepository
from app.schemas.zone import ZoneCreate, ZoneUpdate
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
        raise AppError("zone_create_forbidden", "Only farm owners can perform this action", 403)
    _assert_active_membership(user)


def _assert_farm_scope(user: User, farm_org_id: UUID) -> None:
    if _is_privileged(user):
        return
    if user.organization_id != farm_org_id:
        raise AppError("farm_not_accessible", "Farm is not accessible", 403)


class ZoneService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = ZoneRepository(db)
        self.farm_repo = FarmRepository(db)

    def _get_accessible_farm(self, user: User, farm_id: UUID):
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm:
            raise AppError("parent_farm_not_found", "Farm not found", 404)
        _assert_farm_scope(user, farm.organization_id)
        return farm

    def list_zones(
        self,
        user: User,
        farm_id: UUID | None = None,
        q: str | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Zone], int]:
        page = clamp_page(page)
        page_size = clamp_page_size(page_size)
        offset = calc_offset(page, page_size)

        if farm_id:
            self._get_accessible_farm(user, farm_id)
            zones = self.repo.list_by_farm(farm_id, q, offset, page_size, sort_by, sort_order)
            total = self.repo.count_by_farm(farm_id, q)
        else:
            farms = self.farm_repo.list_by_org(user.organization_id, limit=1000)
            farm_ids = [f.id for f in farms]
            zones = self.repo.list_by_org_farms(farm_ids, q, offset, page_size, sort_by, sort_order)
            total = self.repo.count_by_org_farms(farm_ids, q)

        return zones, total

    def get_zone(self, user: User, zone_id: UUID) -> Zone:
        zone = self.repo.get_by_id(zone_id)
        if not zone:
            raise AppError("zone_not_found", "Zone not found", 404)
        self._get_accessible_farm(user, zone.farm_id)
        return zone

    def create_zone(self, user: User, req: ZoneCreate) -> Zone:
        _assert_owner_write(user)
        self._get_accessible_farm(user, req.farm_id)
        zone = self.repo.create(
            farm_id=req.farm_id,
            name=req.zone_name,
            description=req.description,
        )
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def update_zone(self, user: User, zone_id: UUID, req: ZoneUpdate) -> Zone:
        zone = self.repo.get_by_id(zone_id)
        if not zone:
            raise AppError("zone_not_found", "Zone not found", 404)
        farm = self._get_accessible_farm(user, zone.farm_id)
        if not _is_privileged(user):
            if user.farmer_status != FarmerStatus.owner:
                raise AppError("zone_create_forbidden", "Only farm owners can update zones", 403)

        updates: dict = {}
        if "zone_name" in req.model_fields_set and req.zone_name is not None:
            updates["name"] = req.zone_name
        if "description" in req.model_fields_set:
            updates["description"] = req.description

        if updates:
            zone = self.repo.update(zone, updates)
        self.db.commit()
        self.db.refresh(zone)
        return zone
