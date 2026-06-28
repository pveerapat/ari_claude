from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, db: Session) -> None:
        super().__init__(Notification, db)

    def get_by_id(self, notification_id: UUID) -> Notification | None:
        return (
            self.db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    def list_by_user(
        self,
        user_id: UUID,
        type: Optional[str] = None,
        status: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Notification]:
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        if type:
            query = query.filter(Notification.type == type)
        if status:
            query = query.filter(Notification.status == status)
        return query.order_by(Notification.created_at.desc()).offset(offset).limit(limit).all()

    def count_by_user(
        self,
        user_id: UUID,
        type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> int:
        query = (
            self.db.query(func.count(Notification.id))
            .filter(Notification.user_id == user_id)
        )
        if type:
            query = query.filter(Notification.type == type)
        if status:
            query = query.filter(Notification.status == status)
        return query.scalar() or 0

    def mark_read(self, notification: Notification) -> Notification:
        from app.utils.datetime import utcnow
        notification.status = "read"
        notification.read_at = utcnow()
        self.db.flush()
        return notification

    def mark_all_read(self, user_id: UUID) -> int:
        from app.utils.datetime import utcnow
        now = utcnow()
        updated = (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.status == "unread")
            .all()
        )
        for n in updated:
            n.status = "read"
            n.read_at = now
        self.db.flush()
        return len(updated)
