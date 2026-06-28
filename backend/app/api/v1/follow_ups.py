from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import list_response, success_response
from app.dependencies.auth import require_active_membership
from app.dependencies.db import get_db
from app.models.follow_up import FollowUp
from app.models.user import User
from app.schemas.follow_up import FollowUpCreate, FollowUpUpdate
from app.services.follow_up_service import FollowUpService

router = APIRouter(prefix="/follow-ups", tags=["follow-ups"])


def _follow_up_dict(follow_up: FollowUp) -> dict:
    return {
        "follow_up_id": str(follow_up.id),
        "entry_id": str(follow_up.entry_id),
        "follow_up_day": follow_up.follow_up_day,
        "outcome": follow_up.outcome.value if follow_up.outcome else None,
        "notes": follow_up.notes,
        "recorded_at": follow_up.recorded_at.isoformat() if follow_up.recorded_at else None,
    }


@router.get("")
def list_follow_ups(
    entry_id: Optional[UUID] = Query(None),
    outcome: Optional[str] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="recorded_at"),
    sort_order: str = Query(default="desc"),
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = FollowUpService(db)
    follow_ups, total = svc.list_follow_ups(
        user=user,
        entry_id=entry_id,
        outcome=outcome,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return list_response([_follow_up_dict(f) for f in follow_ups], page, page_size, total)


@router.get("/{follow_up_id}")
def get_follow_up(
    follow_up_id: UUID,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = FollowUpService(db)
    follow_up = svc.get_follow_up(user=user, follow_up_id=follow_up_id)
    return success_response(_follow_up_dict(follow_up))


@router.post("")
def create_follow_up(
    req: FollowUpCreate,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = FollowUpService(db)
    follow_up = svc.create_follow_up(user=user, req=req)
    return success_response(_follow_up_dict(follow_up))


@router.patch("/{follow_up_id}")
def update_follow_up(
    follow_up_id: UUID,
    req: FollowUpUpdate,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = FollowUpService(db)
    follow_up = svc.update_follow_up(user=user, follow_up_id=follow_up_id, req=req)
    return success_response(_follow_up_dict(follow_up))
