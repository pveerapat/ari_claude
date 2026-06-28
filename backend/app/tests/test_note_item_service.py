"""P2-7: Unit tests for NoteItemService — sequence_order and validation rules."""
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.core.enums import FarmerStatus, ItemType, MembershipStatus, UploadStatus, UserRole
from app.core.errors import AppError
from app.services.note_item_service import NoteItemService


def _make_user(org_id=None):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = org_id or uuid4()
    user.role = UserRole.farmer
    user.membership_status = MembershipStatus.active
    return user


def _make_entry(org_id=None):
    entry = MagicMock()
    entry.id = uuid4()
    entry.organization_id = org_id or uuid4()
    return entry


def _make_create_req(item_type=ItemType.photo, seq=None, content_text=None, url=None, file_path=None):
    req = MagicMock()
    req.item_type = item_type
    req.sequence_order = seq
    req.content_text = content_text
    req.file_path = file_path
    req.url = url
    req.platform = None
    req.content_type = None
    req.file_size = None
    req.upload_status = None
    return req


class TestNoteItemSequenceOrder:
    def test_auto_assigns_sequence_order_when_not_provided(self):
        db = MagicMock()
        svc = NoteItemService(db)
        user = _make_user()
        entry = _make_entry(org_id=user.organization_id)
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)
        svc.repo.max_sequence_order = MagicMock(return_value=3)

        req = _make_create_req(item_type=ItemType.photo, seq=None)
        item = MagicMock()
        item.id = uuid4()
        item.sequence_order = 4
        svc.repo.create = MagicMock(return_value=item)
        db.commit = MagicMock()
        db.refresh = MagicMock()

        result = svc.create_item(user, entry.id, req)
        _, kwargs = svc.repo.create.call_args
        assert kwargs["sequence_order"] == 4

    def test_uses_provided_sequence_order(self):
        db = MagicMock()
        svc = NoteItemService(db)
        user = _make_user()
        entry = _make_entry(org_id=user.organization_id)
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)

        req = _make_create_req(item_type=ItemType.photo, seq=10)
        item = MagicMock()
        item.sequence_order = 10
        svc.repo.create = MagicMock(return_value=item)
        db.commit = MagicMock()
        db.refresh = MagicMock()

        svc.create_item(user, entry.id, req)
        _, kwargs = svc.repo.create.call_args
        assert kwargs["sequence_order"] == 10

    def test_auto_assigns_1_for_first_item(self):
        db = MagicMock()
        svc = NoteItemService(db)
        user = _make_user()
        entry = _make_entry(org_id=user.organization_id)
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)
        svc.repo.max_sequence_order = MagicMock(return_value=0)

        req = _make_create_req(item_type=ItemType.text, seq=None, content_text="Observation")
        item = MagicMock()
        item.sequence_order = 1
        svc.repo.create = MagicMock(return_value=item)
        db.commit = MagicMock()
        db.refresh = MagicMock()

        svc.create_item(user, entry.id, req)
        _, kwargs = svc.repo.create.call_args
        assert kwargs["sequence_order"] == 1


class TestNoteItemValidation:
    def test_text_item_requires_content_text(self):
        db = MagicMock()
        svc = NoteItemService(db)
        user = _make_user()
        entry = _make_entry(org_id=user.organization_id)
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)

        req = _make_create_req(item_type=ItemType.text, content_text=None)
        with pytest.raises(AppError) as exc_info:
            svc.create_item(user, entry.id, req)
        assert exc_info.value.status_code == 422
        assert "content_text" in exc_info.value.code

    def test_link_item_requires_url(self):
        db = MagicMock()
        svc = NoteItemService(db)
        user = _make_user()
        entry = _make_entry(org_id=user.organization_id)
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)

        req = _make_create_req(item_type=ItemType.link, url=None)
        with pytest.raises(AppError) as exc_info:
            svc.create_item(user, entry.id, req)
        assert exc_info.value.status_code == 422
        assert "url" in exc_info.value.code

    def test_entry_not_found_blocked(self):
        db = MagicMock()
        svc = NoteItemService(db)
        user = _make_user()
        svc.entry_repo.get_by_id = MagicMock(return_value=None)

        req = _make_create_req()
        with pytest.raises(AppError) as exc_info:
            svc.create_item(user, uuid4(), req)
        assert exc_info.value.status_code == 404

    def test_cross_org_entry_blocked(self):
        db = MagicMock()
        svc = NoteItemService(db)
        user = _make_user()
        entry = _make_entry(org_id=uuid4())
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)

        req = _make_create_req()
        with pytest.raises(AppError) as exc_info:
            svc.create_item(user, entry.id, req)
        assert exc_info.value.status_code == 403

    def test_photo_item_created_without_content_text(self):
        db = MagicMock()
        svc = NoteItemService(db)
        user = _make_user()
        entry = _make_entry(org_id=user.organization_id)
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)
        svc.repo.max_sequence_order = MagicMock(return_value=0)

        req = _make_create_req(item_type=ItemType.photo, file_path="path/to/photo.jpg")
        item = MagicMock()
        item.sequence_order = 1
        svc.repo.create = MagicMock(return_value=item)
        db.commit = MagicMock()
        db.refresh = MagicMock()

        result = svc.create_item(user, entry.id, req)
        assert result is not None


class TestForbiddenScopeAbsence:
    def test_no_consultation_service_import(self):
        import app.services.note_item_service as mod
        assert not hasattr(mod, "ConsultationService")
        assert "consultation" not in dir(mod)

    def test_no_upload_jobs_in_note_item_service(self):
        import app.services.note_item_service as mod
        src = open(mod.__file__).read()
        assert "upload_jobs" not in src

    def test_no_permission_service(self):
        import app.services.notebook_service as mod
        src = open(mod.__file__).read()
        assert "PermissionService" not in src
        assert "permission_service" not in src
