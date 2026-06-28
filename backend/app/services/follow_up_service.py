"""Follow-Up service for P2-7.

Follow-up rules:
- follow_up_day must be 3, 7, or 14.
- outcome must be improved/same/worse/unknown.
- Follow-up is linked to a notebook entry (ideally entry_type=consultation
  per domain model, but the frozen schema does not enforce this at DB level).
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.core.errors import AppError
from app.models.follow_up import FollowUp
from app.models.user import User
from app.repositories.follow_ups import FollowUpRepository
from app.repositories.notebook_entries import NotebookEntryRepository
from app.schemas.follow_up import FollowUpCreate, FollowUpUpdate
from app.services.base import BaseService
from app.utils.pagination import calc_offset, clamp_page, clamp_page_size

_PRIVILEGED_ROLES = {UserRole.admin, UserRole.root, UserRole.ari_staff}

_VALID_DAYS = {3, 7, 14}


def _is_privileged(user: User) -> bool:
    return user.role in _PRIVILEGED_ROLES


class FollowUpService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = FollowUpRepository(db)
        self.entry_repo = NotebookEntryRepository(db)

    def _get_accessible_entry(self, user: User, entry_id: UUID):
        entry = self.entry_repo.get_by_id(entry_id)
        if not entry:
            raise AppError("entry_not_found", "Notebook entry not found", 404)
        if not _is_privileged(user) and entry.organization_id != user.organization_id:
            raise AppError("entry_not_accessible", "Notebook entry is not accessible", 403)
        return entry

    def list_follow_ups(
        self,
        user: User,
        entry_id: Optional[UUID] = None,
        outcome: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "recorded_at",
        sort_order: str = "desc",
    ) -> tuple[list[FollowUp], int]:
        page = clamp_page(page)
        page_size = clamp_page_size(page_size)
        offset = calc_offset(page, page_size)

        privileged = _is_privileged(user)
        follow_ups = self.repo.list_by_user_org(
            user.organization_id, user.id, privileged,
            entry_id, outcome, offset, page_size, sort_by, sort_order,
        )
        total = self.repo.count_by_user_org(
            user.organization_id, user.id, privileged, entry_id, outcome
        )
        return follow_ups, total

    def get_follow_up(self, user: User, follow_up_id: UUID) -> FollowUp:
        follow_up = self.repo.get_by_id(follow_up_id)
        if not follow_up:
            raise AppError("follow_up_not_found", "Follow-up not found", 404)
        self._get_accessible_entry(user, follow_up.entry_id)
        return follow_up

    def create_follow_up(self, user: User, req: FollowUpCreate) -> FollowUp:
        self._get_accessible_entry(user, req.entry_id)
        if req.follow_up_day not in _VALID_DAYS:
            raise AppError(
                "invalid_follow_up_day",
                f"follow_up_day must be one of {sorted(_VALID_DAYS)}",
                422,
            )
        follow_up = self.repo.create(entry_id=req.entry_id, follow_up_day=req.follow_up_day)
        self.db.commit()
        self.db.refresh(follow_up)
        return follow_up

    def update_follow_up(
        self, user: User, follow_up_id: UUID, req: FollowUpUpdate
    ) -> FollowUp:
        follow_up = self.repo.get_by_id(follow_up_id)
        if not follow_up:
            raise AppError("follow_up_not_found", "Follow-up not found", 404)
        self._get_accessible_entry(user, follow_up.entry_id)

        updates: dict = {}
        if "outcome" in req.model_fields_set:
            updates["outcome"] = req.outcome
        if "notes" in req.model_fields_set:
            updates["notes"] = req.notes

        if updates:
            follow_up = self.repo.update(follow_up, updates)
        self.db.commit()
        self.db.refresh(follow_up)
        return follow_up
