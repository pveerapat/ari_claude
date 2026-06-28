"""Notebook Entry service for P2-7.

Hierarchy validation rules (frozen):
- farm must belong to organization
- zone must belong to farm (if both provided)
- tree must belong to zone (if both provided)
- farm_id/zone_id/tree_id are all nullable

API-GAP-P2-7-001: Inference of parent IDs (zone without farm, tree without zone)
is NOT performed. Explicit parent IDs are required when child IDs are provided.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.core.errors import AppError
from app.models.notebook_entry import NotebookEntry
from app.models.user import User
from app.repositories.farms import FarmRepository
from app.repositories.notebook_entries import NotebookEntryRepository
from app.repositories.zones import ZoneRepository
from app.repositories.trees import TreeRepository
from app.schemas.notebook_entry import NotebookEntryCreate, NotebookEntryUpdate
from app.services.base import BaseService
from app.utils.pagination import calc_offset, clamp_page, clamp_page_size

_PRIVILEGED_ROLES = {UserRole.admin, UserRole.root, UserRole.ari_staff}


def _is_privileged(user: User) -> bool:
    return user.role in _PRIVILEGED_ROLES


class NotebookService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = NotebookEntryRepository(db)
        self.farm_repo = FarmRepository(db)
        self.zone_repo = ZoneRepository(db)
        self.tree_repo = TreeRepository(db)

    def _validate_hierarchy(
        self,
        organization_id: UUID,
        farm_id: Optional[UUID],
        zone_id: Optional[UUID],
        tree_id: Optional[UUID],
    ) -> None:
        if farm_id:
            farm = self.farm_repo.get_by_id(farm_id)
            if not farm:
                raise AppError("farm_not_found", "Farm not found", 404)
            if farm.organization_id != organization_id:
                raise AppError("farm_not_in_org", "Farm does not belong to the organization", 403)

        if zone_id:
            if not farm_id:
                raise AppError(
                    "farm_id_required",
                    "farm_id is required when zone_id is provided. "
                    "See API-GAP-P2-7-001.",
                    422,
                )
            zone = self.zone_repo.get_by_id(zone_id)
            if not zone:
                raise AppError("zone_not_found", "Zone not found", 404)
            if zone.farm_id != farm_id:
                raise AppError("zone_not_in_farm", "Zone does not belong to the farm", 403)

        if tree_id:
            if not zone_id:
                raise AppError(
                    "zone_id_required",
                    "zone_id is required when tree_id is provided. "
                    "See API-GAP-P2-7-001.",
                    422,
                )
            tree = self.tree_repo.get_by_id(tree_id)
            if not tree:
                raise AppError("tree_not_found", "Tree not found", 404)
            if tree.zone_id != zone_id:
                raise AppError("tree_not_in_zone", "Tree does not belong to the zone", 403)

    def _assert_org_scope(self, user: User, organization_id: UUID) -> None:
        if _is_privileged(user):
            return
        if user.organization_id != organization_id:
            raise AppError("organization_not_accessible", "Organization is not accessible", 403)

    def _assert_entry_access(self, user: User, entry: NotebookEntry) -> None:
        self._assert_org_scope(user, entry.organization_id)

    def list_entries(
        self,
        user: User,
        organization_id: Optional[UUID] = None,
        farm_id: Optional[UUID] = None,
        zone_id: Optional[UUID] = None,
        tree_id: Optional[UUID] = None,
        entry_type: Optional[str] = None,
        entry_context: Optional[str] = None,
        analysis_status: Optional[str] = None,
        created_by_user_id: Optional[UUID] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        q: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[NotebookEntry], int]:
        page = clamp_page(page)
        page_size = clamp_page_size(page_size)
        offset = calc_offset(page, page_size)

        scope_org = organization_id if _is_privileged(user) and organization_id else user.organization_id
        if not _is_privileged(user) and organization_id and organization_id != user.organization_id:
            raise AppError("organization_not_accessible", "Organization is not accessible", 403)

        entries = self.repo.list_by_org(
            scope_org, farm_id, zone_id, tree_id, entry_type, entry_context,
            analysis_status, created_by_user_id, date_from, date_to, q,
            offset, page_size, sort_by, sort_order,
        )
        total = self.repo.count_by_org(
            scope_org, farm_id, zone_id, tree_id, entry_type, entry_context,
            analysis_status, created_by_user_id, date_from, date_to, q,
        )
        return entries, total

    def get_entry(self, user: User, entry_id: UUID) -> NotebookEntry:
        entry = self.repo.get_by_id(entry_id)
        if not entry:
            raise AppError("entry_not_found", "Notebook entry not found", 404)
        self._assert_entry_access(user, entry)
        return entry

    def create_entry(self, user: User, req: NotebookEntryCreate) -> NotebookEntry:
        self._assert_org_scope(user, req.organization_id)
        self._validate_hierarchy(req.organization_id, req.farm_id, req.zone_id, req.tree_id)

        entry = self.repo.create(
            organization_id=req.organization_id,
            created_by_user_id=user.id,
            entry_type=req.entry_type,
            entry_context=req.entry_context,
            farm_id=req.farm_id,
            zone_id=req.zone_id,
            tree_id=req.tree_id,
            title=req.title,
            summary=req.summary,
            analysis_status=req.analysis_status or "not_started",
            external_ai=req.ai_provider,
            ai_usefulness_status=req.ai_usefulness_status,
            learned_summary=req.learned_summary,
        )
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def update_entry(self, user: User, entry_id: UUID, req: NotebookEntryUpdate) -> NotebookEntry:
        entry = self.repo.get_by_id(entry_id)
        if not entry:
            raise AppError("entry_not_found", "Notebook entry not found", 404)
        self._assert_entry_access(user, entry)

        new_farm_id = entry.farm_id
        new_zone_id = entry.zone_id
        new_tree_id = entry.tree_id

        if "farm_id" in req.model_fields_set:
            new_farm_id = req.farm_id
        if "zone_id" in req.model_fields_set:
            new_zone_id = req.zone_id
        if "tree_id" in req.model_fields_set:
            new_tree_id = req.tree_id

        self._validate_hierarchy(entry.organization_id, new_farm_id, new_zone_id, new_tree_id)

        updates: dict = {}
        if "title" in req.model_fields_set:
            updates["title"] = req.title
        if "summary" in req.model_fields_set:
            updates["summary"] = req.summary
        if "farm_id" in req.model_fields_set:
            updates["farm_id"] = req.farm_id
        if "zone_id" in req.model_fields_set:
            updates["zone_id"] = req.zone_id
        if "tree_id" in req.model_fields_set:
            updates["tree_id"] = req.tree_id
        if "analysis_status" in req.model_fields_set:
            updates["analysis_status"] = req.analysis_status
        if "ai_provider" in req.model_fields_set:
            updates["external_ai"] = req.ai_provider
        if "ai_usefulness_status" in req.model_fields_set:
            updates["ai_usefulness_status"] = req.ai_usefulness_status
        if "learned_summary" in req.model_fields_set:
            updates["learned_summary"] = req.learned_summary

        if updates:
            entry = self.repo.update(entry, updates)
        self.db.commit()
        self.db.refresh(entry)
        return entry
