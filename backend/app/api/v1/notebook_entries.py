from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import list_response, success_response
from app.dependencies.auth import require_active_account, require_active_membership
from app.dependencies.db import get_db
from app.models.notebook_entry import NotebookEntry
from app.models.user import User
from app.schemas.notebook_entry import NotebookEntryCreate, NotebookEntryUpdate
from app.services.notebook_service import NotebookService

router = APIRouter(prefix="/notebook-entries", tags=["notebook-entries"])


def _entry_dict(entry: NotebookEntry) -> dict:
    return {
        "entry_id": str(entry.id),
        "organization_id": str(entry.organization_id),
        "created_by_user_id": str(entry.created_by_user_id),
        "farm_id": str(entry.farm_id) if entry.farm_id else None,
        "zone_id": str(entry.zone_id) if entry.zone_id else None,
        "tree_id": str(entry.tree_id) if entry.tree_id else None,
        "entry_type": entry.entry_type.value if entry.entry_type else None,
        "entry_context": entry.entry_context.value if entry.entry_context else None,
        "title": entry.title,
        "summary": entry.summary,
        "suggested_category": entry.suggested_category,
        "analysis_status": entry.analysis_status,
        "ai_provider": entry.external_ai.value if entry.external_ai else None,
        "ai_usefulness_status": entry.ai_usefulness_status,
        "learned_summary": entry.learned_summary,
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
        "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
    }


@router.get("")
def list_notebook_entries(
    organization_id: Optional[UUID] = Query(None),
    farm_id: Optional[UUID] = Query(None),
    zone_id: Optional[UUID] = Query(None),
    tree_id: Optional[UUID] = Query(None),
    entry_type: Optional[str] = Query(None),
    entry_context: Optional[str] = Query(None),
    analysis_status: Optional[str] = Query(None),
    created_by_user_id: Optional[UUID] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = NotebookService(db)
    entries, total = svc.list_entries(
        user=user,
        organization_id=organization_id,
        farm_id=farm_id,
        zone_id=zone_id,
        tree_id=tree_id,
        entry_type=entry_type,
        entry_context=entry_context,
        analysis_status=analysis_status,
        created_by_user_id=created_by_user_id,
        date_from=date_from,
        date_to=date_to,
        q=q,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return list_response([_entry_dict(e) for e in entries], page, page_size, total)


@router.get("/{entry_id}")
def get_notebook_entry(
    entry_id: UUID,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = NotebookService(db)
    entry = svc.get_entry(user=user, entry_id=entry_id)
    return success_response(_entry_dict(entry))


@router.post("")
def create_notebook_entry(
    req: NotebookEntryCreate,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = NotebookService(db)
    entry = svc.create_entry(user=user, req=req)
    return success_response(_entry_dict(entry))


@router.patch("/{entry_id}")
def update_notebook_entry(
    entry_id: UUID,
    req: NotebookEntryUpdate,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = NotebookService(db)
    entry = svc.update_entry(user=user, entry_id=entry_id, req=req)
    return success_response(_entry_dict(entry))
