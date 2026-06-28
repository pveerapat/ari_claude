"""P2-7: API-level tests for Sync batch endpoint."""
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.dependencies.auth import require_active_membership
from app.dependencies.db import get_db
from app.main import app
from app.schemas.sync import SyncBatchResponse, SyncItemResult


def _mock_db():
    yield MagicMock()


@pytest.fixture(autouse=True)
def override_db():
    app.dependency_overrides[get_db] = _mock_db
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def client():
    return TestClient(app)


def _make_active_farmer(org_id=None):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = org_id or uuid4()
    user.role = UserRole.farmer
    user.farmer_status = FarmerStatus.owner
    user.membership_status = MembershipStatus.active
    user.account_status = AccountStatus.active
    return user


_BATCH_PAYLOAD = {
    "device_id": str(uuid4()),
    "client_batch_id": str(uuid4()),
    "items": [
        {
            "client_id": str(uuid4()),
            "entity_type": "notebook_entry",
            "action": "create",
            "payload": {
                "organization_id": str(uuid4()),
                "entry_type": "note",
                "entry_context": "general_note",
            },
        }
    ],
}


class TestSyncBatch:
    def test_active_user_can_sync(self, client):
        user = _make_active_farmer()
        client_id = uuid4()
        batch_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.sync.SyncService") as MockSvc:
            MockSvc.return_value.process_batch.return_value = SyncBatchResponse(
                client_batch_id=batch_id,
                results=[
                    SyncItemResult(
                        client_id=client_id,
                        server_id=uuid4(),
                        status="completed",
                    )
                ],
            )
            resp = client.post("/api/v1/sync/batch", json={
                "device_id": str(uuid4()),
                "client_batch_id": str(batch_id),
                "items": [{
                    "client_id": str(client_id),
                    "entity_type": "notebook_entry",
                    "action": "create",
                    "payload": {
                        "organization_id": str(user.organization_id),
                        "entry_type": "note",
                        "entry_context": "general_note",
                    },
                }],
            })
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "client_batch_id" in data
        assert "results" in data
        assert data["results"][0]["status"] == "completed"

    def test_sync_returns_per_item_results(self, client):
        user = _make_active_farmer()
        client_id_1 = uuid4()
        client_id_2 = uuid4()
        batch_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.sync.SyncService") as MockSvc:
            MockSvc.return_value.process_batch.return_value = SyncBatchResponse(
                client_batch_id=batch_id,
                results=[
                    SyncItemResult(client_id=client_id_1, server_id=uuid4(), status="completed"),
                    SyncItemResult(client_id=client_id_2, status="failed", error="entry error"),
                ],
            )
            resp = client.post("/api/v1/sync/batch", json={
                "device_id": str(uuid4()),
                "client_batch_id": str(batch_id),
                "items": [
                    {
                        "client_id": str(client_id_1),
                        "entity_type": "notebook_entry",
                        "action": "create",
                        "payload": {"organization_id": str(user.organization_id)},
                    },
                    {
                        "client_id": str(client_id_2),
                        "entity_type": "notebook_entry",
                        "action": "create",
                        "payload": {},
                    },
                ],
            })
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        results = resp.json()["data"]["results"]
        assert len(results) == 2
        statuses = {r["client_id"]: r["status"] for r in results}
        assert statuses[str(client_id_1)] == "completed"
        assert statuses[str(client_id_2)] == "failed"

    def test_unauthenticated_blocked(self, client):
        resp = client.post("/api/v1/sync/batch", json=_BATCH_PAYLOAD)
        assert resp.status_code in (401, 403)

    def test_pending_membership_blocked(self, client):
        def _pending():
            raise AppError("membership_not_active", "not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        resp = client.post("/api/v1/sync/batch", json=_BATCH_PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_sync_uses_items_action_format(self, client):
        user = _make_active_farmer()
        batch_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.sync.SyncService") as MockSvc:
            MockSvc.return_value.process_batch.return_value = SyncBatchResponse(
                client_batch_id=batch_id,
                results=[],
            )
            resp = client.post("/api/v1/sync/batch", json={
                "device_id": str(uuid4()),
                "client_batch_id": str(batch_id),
                "items": [],
            })
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        _, kwargs = MockSvc.return_value.process_batch.call_args
        req = kwargs["req"]
        assert hasattr(req, "items")

    def test_operations_format_not_accepted(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        resp = client.post("/api/v1/sync/batch", json={
            "device_id": str(uuid4()),
            "client_batch_id": str(uuid4()),
            "operations": [{"client_id": str(uuid4()), "operation_type": "create_notebook_entry"}],
        })
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 422
