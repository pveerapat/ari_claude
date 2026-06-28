from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.models.tree import Tree
from app.models.user import User
from app.repositories.farms import FarmRepository
from app.repositories.trees import TreeRepository
from app.repositories.zones import ZoneRepository
from app.schemas.tree import TreeCreate, TreeUpdate
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
        raise AppError("tree_create_forbidden", "Only farm owners can perform this action", 403)
    _assert_active_membership(user)


def _assert_farm_scope(user: User, farm_org_id: UUID) -> None:
    if _is_privileged(user):
        return
    if user.organization_id != farm_org_id:
        raise AppError("farm_not_accessible", "Farm is not accessible", 403)


class TreeService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = TreeRepository(db)
        self.zone_repo = ZoneRepository(db)
        self.farm_repo = FarmRepository(db)

    def _get_accessible_zone(self, user: User, zone_id: UUID):
        zone = self.zone_repo.get_by_id(zone_id)
        if not zone:
            raise AppError("parent_zone_not_found", "Zone not found", 404)
        farm = self.farm_repo.get_by_id(zone.farm_id)
        if not farm:
            raise AppError("parent_farm_not_found", "Farm not found", 404)
        _assert_farm_scope(user, farm.organization_id)
        return zone, farm

    def list_trees(
        self,
        user: User,
        zone_id: UUID | None = None,
        farm_id: UUID | None = None,
        status: str | None = None,
        q: str | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Tree], int]:
        page = clamp_page(page)
        page_size = clamp_page_size(page_size)
        offset = calc_offset(page, page_size)

        if zone_id:
            self._get_accessible_zone(user, zone_id)
            trees = self.repo.list_by_zone(zone_id, status, q, offset, page_size, sort_by, sort_order)
            total = self.repo.count_by_zone(zone_id, status, q)
        elif farm_id:
            farm = self.farm_repo.get_by_id(farm_id)
            if not farm:
                raise AppError("farm_not_found", "Farm not found", 404)
            _assert_farm_scope(user, farm.organization_id)
            trees = self.repo.list_by_farm(farm_id, status, q, offset, page_size, sort_by, sort_order)
            total = self.repo.count_by_farm(farm_id, status, q)
        else:
            trees = []
            total = 0

        return trees, total

    def get_tree(self, user: User, tree_id: UUID) -> Tree:
        tree = self.repo.get_by_id(tree_id)
        if not tree:
            raise AppError("tree_not_found", "Tree not found", 404)
        self._get_accessible_zone(user, tree.zone_id)
        return tree

    def create_tree(self, user: User, req: TreeCreate) -> Tree:
        _assert_owner_write(user)
        self._get_accessible_zone(user, req.zone_id)
        tree = self.repo.create(
            zone_id=req.zone_id,
            tree_code=req.tree_code,
            status=req.status,
        )
        self.db.commit()
        self.db.refresh(tree)
        return tree

    def update_tree(self, user: User, tree_id: UUID, req: TreeUpdate) -> Tree:
        tree = self.repo.get_by_id(tree_id)
        if not tree:
            raise AppError("tree_not_found", "Tree not found", 404)
        self._get_accessible_zone(user, tree.zone_id)
        if not _is_privileged(user):
            if user.farmer_status != FarmerStatus.owner:
                raise AppError("tree_create_forbidden", "Only farm owners can update trees", 403)

        updates: dict = {}
        if "tree_code" in req.model_fields_set and req.tree_code is not None:
            updates["tree_code"] = req.tree_code
        if "status" in req.model_fields_set:
            updates["status"] = req.status

        if updates:
            tree = self.repo.update(tree, updates)
        self.db.commit()
        self.db.refresh(tree)
        return tree
