from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import list_response, success_response
from app.dependencies.auth import require_active_membership
from app.dependencies.db import get_db
from app.models.note_item import NoteItem
from app.models.user import User
from app.schemas.note_item import NoteItemCreate, NoteItemUpdate
from app.services.note_item_service import NoteItemService

router = APIRouter(tags=["note-items"])


def _item_dict(item: NoteItem) -> dict:
    return {
        "item_id": str(item.id),
        "entry_id": str(item.entry_id),
        "item_type": item.item_type.value if item.item_type else None,
        "sequence_order": item.sequence_order,
        "content_text": item.content_text,
        "file_path": item.file_path,
        "url": item.url,
        "platform": item.platform,
        "upload_status": item.upload_status.value if item.upload_status else None,
        "created_at": item.created_at.isoformat() if item.created_at else None,
    }


@router.get("/notebook-entries/{entry_id}/items")
def list_note_items(
    entry_id: UUID,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = NoteItemService(db)
    items = svc.list_items(user=user, entry_id=entry_id)
    return list_response([_item_dict(i) for i in items], 1, len(items), len(items))


@router.post("/notebook-entries/{entry_id}/items")
def create_note_item(
    entry_id: UUID,
    req: NoteItemCreate,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = NoteItemService(db)
    item = svc.create_item(user=user, entry_id=entry_id, req=req)
    return success_response(_item_dict(item))


@router.patch("/note-items/{item_id}")
def update_note_item(
    item_id: UUID,
    req: NoteItemUpdate,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = NoteItemService(db)
    item = svc.update_item(user=user, item_id=item_id, req=req)
    return success_response(_item_dict(item))
