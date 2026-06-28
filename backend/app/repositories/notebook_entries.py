from typing import Optional
from uuid import UUID

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.notebook_entry import NotebookEntry
from app.repositories.base import BaseRepository


class NotebookEntryRepository(BaseRepository[NotebookEntry]):
    def __init__(self, db: Session) -> None:
        super().__init__(NotebookEntry, db)

    def get_by_id(self, entry_id: UUID) -> NotebookEntry | None:
        return self.db.query(NotebookEntry).filter(NotebookEntry.id == entry_id).first()

    def list_by_org(
        self,
        organization_id: UUID,
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
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[NotebookEntry]:
        query = self.db.query(NotebookEntry).filter(
            NotebookEntry.organization_id == organization_id
        )
        query = self._apply_filters(
            query, farm_id, zone_id, tree_id, entry_type, entry_context,
            analysis_status, created_by_user_id, date_from, date_to, q
        )
        col = getattr(NotebookEntry, sort_by, NotebookEntry.created_at)
        order = col.desc() if sort_order == "desc" else col.asc()
        return query.order_by(order).offset(offset).limit(limit).all()

    def count_by_org(
        self,
        organization_id: UUID,
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
    ) -> int:
        query = self.db.query(func.count(NotebookEntry.id)).filter(
            NotebookEntry.organization_id == organization_id
        )
        query = self._apply_filters(
            query, farm_id, zone_id, tree_id, entry_type, entry_context,
            analysis_status, created_by_user_id, date_from, date_to, q
        )
        return query.scalar() or 0

    def _apply_filters(self, query, farm_id, zone_id, tree_id, entry_type,
                       entry_context, analysis_status, created_by_user_id,
                       date_from, date_to, q):
        if farm_id:
            query = query.filter(NotebookEntry.farm_id == farm_id)
        if zone_id:
            query = query.filter(NotebookEntry.zone_id == zone_id)
        if tree_id:
            query = query.filter(NotebookEntry.tree_id == tree_id)
        if entry_type:
            query = query.filter(NotebookEntry.entry_type == entry_type)
        if entry_context:
            query = query.filter(NotebookEntry.entry_context == entry_context)
        if analysis_status:
            query = query.filter(NotebookEntry.analysis_status == analysis_status)
        if created_by_user_id:
            query = query.filter(NotebookEntry.created_by_user_id == created_by_user_id)
        if date_from:
            query = query.filter(NotebookEntry.created_at >= date_from)
        if date_to:
            query = query.filter(NotebookEntry.created_at <= date_to)
        if q:
            query = query.filter(
                or_(
                    NotebookEntry.title.ilike(f"%{q}%"),
                    NotebookEntry.summary.ilike(f"%{q}%"),
                )
            )
        return query

    def create(
        self,
        organization_id: UUID,
        created_by_user_id: UUID,
        entry_type: str,
        entry_context: str,
        farm_id: Optional[UUID] = None,
        zone_id: Optional[UUID] = None,
        tree_id: Optional[UUID] = None,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        analysis_status: str = "not_started",
        external_ai=None,
        ai_usefulness_status: Optional[str] = None,
        learned_summary: Optional[str] = None,
    ) -> NotebookEntry:
        entry = NotebookEntry(
            organization_id=organization_id,
            created_by_user_id=created_by_user_id,
            entry_type=entry_type,
            entry_context=entry_context,
            farm_id=farm_id,
            zone_id=zone_id,
            tree_id=tree_id,
            title=title,
            summary=summary,
            analysis_status=analysis_status,
            external_ai=external_ai,
            ai_usefulness_status=ai_usefulness_status,
            learned_summary=learned_summary,
        )
        self.db.add(entry)
        self.db.flush()
        return entry

    def update(self, entry: NotebookEntry, updates: dict) -> NotebookEntry:
        for key, value in updates.items():
            setattr(entry, key, value)
        self.db.flush()
        return entry
