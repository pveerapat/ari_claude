from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from app.main import app
from app.core.constants import SERVICE_NAME, API_V1_PREFIX, REQUEST_ID_HEADER
from app.core.errors import AppError
from app.core.response import error_response, list_response, success_response
from app.utils.pagination import calc_offset, pagination_meta
from app.utils.uuid import generate_uuid, is_valid_uuid


def test_app_is_not_none():
    assert app is not None


def test_app_title():
    assert "ARI" in app.title


def test_constants():
    assert SERVICE_NAME == "ari-backend"
    assert API_V1_PREFIX == "/api/v1"
    assert REQUEST_ID_HEADER == "X-Request-ID"


def test_success_response_shape():
    result = success_response({"id": "1"})
    assert "data" in result
    assert result["data"] == {"id": "1"}


def test_list_response_shape():
    result = list_response([], page=1, page_size=20, total_records=0)
    assert "data" in result
    assert "pagination" in result
    assert result["pagination"]["page"] == 1


def test_error_response_shape():
    result = error_response("not_found", "Resource not found")
    assert "error" in result
    assert result["error"]["code"] == "not_found"
    assert result["error"]["message"] == "Resource not found"


def test_error_response_with_request_id():
    result = error_response("not_found", "Resource not found", "req-abc")
    assert result["error"]["request_id"] == "req-abc"


def test_app_error_class():
    err = AppError("not_found", "Not found", status_code=404)
    assert err.code == "not_found"
    assert err.status_code == 404


def test_generate_uuid():
    uid = generate_uuid()
    assert isinstance(uid, str)
    assert is_valid_uuid(uid)


def test_is_valid_uuid_false():
    assert not is_valid_uuid("not-a-uuid")


def test_pagination_meta():
    meta = pagination_meta(page=1, page_size=20, total_records=45)
    assert meta["total_pages"] == 3


def test_calc_offset():
    assert calc_offset(page=2, page_size=20) == 20


def test_no_feature_routes():
    route_paths = [route.path for route in app.routes if isinstance(route, APIRoute)]
    forbidden = [
        "/api/v1/auth",
        "/api/v1/users",
        "/api/v1/organizations",
        "/api/v1/farms",
        "/api/v1/zones",
        "/api/v1/trees",
        "/api/v1/notebook_entries",
        "/api/v1/note_items",
        "/api/v1/follow_ups",
        "/api/v1/notifications",
        "/api/v1/upload_queue",
        "/api/v1/files",
        "/api/v1/sync",
    ]
    for path in forbidden:
        assert path not in route_paths


def test_health_with_test_client():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
