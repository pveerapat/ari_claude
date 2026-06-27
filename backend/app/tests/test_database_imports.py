"""P2-4: verify all frozen models and enums can be imported without error."""

from app.core.enums import (
    AccountStatus,
    EntryContext,
    EntryType,
    ExternalAI,
    FarmerStatus,
    FollowUpOutcome,
    ItemType,
    MembershipStatus,
    UploadStatus,
    UserRole,
)
from app.db.base import Base
from app.models import (
    Farm,
    FollowUp,
    NoteItem,
    NotebookEntry,
    Notification,
    Organization,
    Tree,
    UploadJob,
    User,
    Zone,
)


class TestEnumImports:
    def test_user_role_values(self):
        assert set(UserRole) == {
            UserRole.farmer, UserRole.ari_staff, UserRole.farm_coordinator,
            UserRole.agronomist, UserRole.reviewer, UserRole.admin, UserRole.root,
        }

    def test_entry_type_values(self):
        assert set(EntryType) == {EntryType.note, EntryType.consultation}

    def test_entry_context_values(self):
        assert set(EntryContext) == {
            EntryContext.general_note, EntryContext.registered_farm,
            EntryContext.external_observation, EntryContext.interview,
        }

    def test_item_type_values(self):
        assert set(ItemType) == {
            ItemType.photo, ItemType.video, ItemType.voice,
            ItemType.text, ItemType.file, ItemType.link,
        }

    def test_external_ai_values(self):
        assert set(ExternalAI) == {
            ExternalAI.chatgpt, ExternalAI.gemini, ExternalAI.claude, ExternalAI.other,
        }

    def test_upload_status_values(self):
        assert set(UploadStatus) == {
            UploadStatus.pending, UploadStatus.uploading,
            UploadStatus.failed, UploadStatus.completed,
        }

    def test_follow_up_outcome_values(self):
        assert set(FollowUpOutcome) == {
            FollowUpOutcome.improved, FollowUpOutcome.same,
            FollowUpOutcome.worse, FollowUpOutcome.unknown,
        }

    def test_farmer_status_values(self):
        assert set(FarmerStatus) == {
            FarmerStatus.owner, FarmerStatus.owner_family, FarmerStatus.farm_staff,
        }

    def test_membership_status_values(self):
        assert set(MembershipStatus) == {
            MembershipStatus.pending_farm_approval, MembershipStatus.active,
            MembershipStatus.rejected, MembershipStatus.suspended, MembershipStatus.revoked,
        }

    def test_account_status_values(self):
        assert set(AccountStatus) == {
            AccountStatus.active, AccountStatus.active_pending_verification,
            AccountStatus.pending_review, AccountStatus.suspended,
            AccountStatus.rejected, AccountStatus.revoked,
        }


class TestModelImports:
    def test_organization_importable(self):
        assert Organization is not None
        assert Organization.__tablename__ == "organizations"

    def test_farm_importable(self):
        assert Farm is not None
        assert Farm.__tablename__ == "farms"

    def test_user_importable(self):
        assert User is not None
        assert User.__tablename__ == "users"

    def test_zone_importable(self):
        assert Zone is not None
        assert Zone.__tablename__ == "zones"

    def test_tree_importable(self):
        assert Tree is not None
        assert Tree.__tablename__ == "trees"

    def test_notebook_entry_importable(self):
        assert NotebookEntry is not None
        assert NotebookEntry.__tablename__ == "notebook_entries"

    def test_note_item_importable(self):
        assert NoteItem is not None
        assert NoteItem.__tablename__ == "note_items"

    def test_follow_up_importable(self):
        assert FollowUp is not None
        assert FollowUp.__tablename__ == "follow_ups"

    def test_notification_importable(self):
        assert Notification is not None
        assert Notification.__tablename__ == "notifications"

    def test_upload_job_importable(self):
        assert UploadJob is not None
        assert UploadJob.__tablename__ == "upload_queue"

    def test_base_importable(self):
        assert Base is not None
