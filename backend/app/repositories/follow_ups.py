from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.enums import FollowUpOutcome
from app.models.follow_up import FollowUp
from app.repositories.base import BaseRepository


class FollowUpRepository(BaseRepository[FollowUp]):
    def __init__(self, db: Session) -> None:
        super().__init__(FollowUp, db)

    def get_by_id(self, follow_up_id: UUID) -> FollowUp | None:
        return self.db.query(FollowUp).filter(FollowUp.id == follow_up_id).first()

    def list_by_user_org(
        self,
        organization_id: UUID,
        user_id: UUID,
        is_privileged: bool,
        entry_id: Optional[UUID] = None,
        outcome: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "recorded_at",
        sort_order: str = "desc",
    ) -> list[FollowUp]:
        from app.models.notebook_entry import NotebookEntry
        query = (
            self.db.query(FollowUp)
            .join(NotebookEntry, FollowUp.entry_id == NotebookEntry.id)
            .filter(NotebookEntry.organization_id == organization_id)
        )
        if not is_privileged:
            query = query.filter(NotebookEntry.created_by_user_id == user_id)
        if entry_id:
            query = query.filter(FollowUp.entry_id == entry_id)
        if outcome:
            query = query.filter(FollowUp.outcome == outcome)
        col = getattr(FollowUp, sort_by, FollowUp.recorded_at)
        order = col.desc() if sort_order == "desc" else col.asc()
        return query.order_by(order).offset(offset).limit(limit).all()

    def count_by_user_org(
        self,
        organization_id: UUID,
        user_id: UUID,
        is_privileged: bool,
        entry_id: Optional[UUID] = None,
        outcome: Optional[str] = None,
    ) -> int:
        from app.models.notebook_entry import NotebookEntry
        query = (
            self.db.query(func.count(FollowUp.id))
            .join(NotebookEntry, FollowUp.entry_id == NotebookEntry.id)
            .filter(NotebookEntry.organization_id == organization_id)
        )
        if not is_privileged:
            query = query.filter(NotebookEntry.created_by_user_id == user_id)
        if entry_id:
            query = query.filter(FollowUp.entry_id == entry_id)
        if outcome:
            query = query.filter(FollowUp.outcome == outcome)
        return query.scalar() or 0

    def create(self, entry_id: UUID, follow_up_day: int) -> FollowUp:
        follow_up = FollowUp(entry_id=entry_id, follow_up_day=follow_up_day)
        self.db.add(follow_up)
        self.db.flush()
        return follow_up

    def update(self, follow_up: FollowUp, updates: dict) -> FollowUp:
        for key, value in updates.items():
            setattr(follow_up, key, value)
        self.db.flush()
        return follow_up
