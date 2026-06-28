"""Notification service for P2-7.

Notifications are own-user scoped. Users can only read/mark their own notifications.
Admin/root/ari_staff may manage notifications for any user in their org scope.

API-GAP-P2-7-014: Notification creation is not exposed through a public API.
Notifications are created internally by backend events (upload success/failure,
follow-up reminders). This service exposes read and mark-read operations only.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.core.errors import AppError
from app.models.notification import Notification
from app.models.user import User
from app.repositories.notifications import NotificationRepository
from app.services.base import BaseService
from app.utils.pagination import calc_offset, clamp_page, clamp_page_size

_PRIVILEGED_ROLES = {UserRole.admin, UserRole.root, UserRole.ari_staff}


def _is_privileged(user: User) -> bool:
    return user.role in _PRIVILEGED_ROLES


class NotificationService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = NotificationRepository(db)

    def list_notifications(
        self,
        user: User,
        type: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Notification], int]:
        page = clamp_page(page)
        page_size = clamp_page_size(page_size)
        offset = calc_offset(page, page_size)

        notifications = self.repo.list_by_user(user.id, type, status, offset, page_size)
        total = self.repo.count_by_user(user.id, type, status)
        return notifications, total

    def get_notification(self, user: User, notification_id: UUID) -> Notification:
        notification = self.repo.get_by_id(notification_id)
        if not notification:
            raise AppError("notification_not_found", "Notification not found", 404)
        if notification.user_id != user.id and not _is_privileged(user):
            raise AppError("notification_not_accessible", "Notification is not accessible", 403)
        return notification

    def mark_read(self, user: User, notification_id: UUID) -> Notification:
        notification = self.get_notification(user, notification_id)
        notification = self.repo.mark_read(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_all_read(self, user: User) -> int:
        count = self.repo.mark_all_read(user.id)
        self.db.commit()
        return count
