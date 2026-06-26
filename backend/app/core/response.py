import math
from typing import Any


def success_response(data: Any) -> dict:
    return {"data": data}


def list_response(data: list, page: int, page_size: int, total_records: int) -> dict:
    total_pages = math.ceil(total_records / page_size) if page_size > 0 else 0
    return {
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_records": total_records,
            "total_pages": total_pages,
        },
    }


def error_response(code: str, message: str, request_id: str | None = None) -> dict:
    error: dict[str, Any] = {"code": code, "message": message}
    if request_id is not None:
        error["request_id"] = request_id
    return {"error": error}
