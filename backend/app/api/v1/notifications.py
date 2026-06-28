from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import list_response, success_response
from app.dependencies.auth import require_active_account
from app.dependencies.db import get_db
from app.models.notification import Notification
from app.models.user import User
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


def _notification_dict(n: Notification) -> dict:
    return {
        "notification_id": str(n.id),
        "user_id": str(n.user_id),
        "type": n.type,
        "message": n.message,
        "status": n.status,
        "read_at": n.read_at.isoformat() if n.read_at else None,
        "created_at": n.created_at.isoformat() if n.created_at else None,
    }


@router.get("")
def list_notifications(
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = NotificationService(db)
    notifications, total = svc.list_notifications(
        user=user, type=type, status=status, page=page, page_size=page_size
    )
    return list_response([_notification_dict(n) for n in notifications], page, page_size, total)


@router.get("/{notification_id}")
def get_notification(
    notification_id: UUID,
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = NotificationService(db)
    notification = svc.get_notification(user=user, notification_id=notification_id)
    return success_response(_notification_dict(notification))


@router.patch("/{notification_id}/read")
def mark_notification_read(
    notification_id: UUID,
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = NotificationService(db)
    notification = svc.mark_read(user=user, notification_id=notification_id)
    return success_response(_notification_dict(notification))


@router.post("/mark-all-read")
def mark_all_notifications_read(
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = NotificationService(db)
    updated_count = svc.mark_all_read(user=user)
    return success_response({"success": True, "updated_count": updated_count})
