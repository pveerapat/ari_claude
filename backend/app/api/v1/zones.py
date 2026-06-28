from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import list_response, success_response
from app.dependencies.auth import require_active_account, require_active_membership
from app.dependencies.db import get_db
from app.models.user import User
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneUpdate
from app.services.zone_service import ZoneService

router = APIRouter(prefix="/zones", tags=["zones"])


def _zone_dict(zone: Zone) -> dict:
    return {
        "zone_id": str(zone.id),
        "farm_id": str(zone.farm_id),
        "zone_name": zone.name,
        "description": zone.description,
        "created_at": zone.created_at.isoformat() if zone.created_at else None,
        "updated_at": zone.updated_at.isoformat() if zone.updated_at else None,
    }


@router.get("")
def list_zones(
    farm_id: Optional[UUID] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
    q: Optional[str] = Query(None),
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = ZoneService(db)
    zones, total = svc.list_zones(
        user=user,
        farm_id=farm_id,
        q=q,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return list_response([_zone_dict(z) for z in zones], page, page_size, total)


@router.get("/{zone_id}")
def get_zone(
    zone_id: UUID,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = ZoneService(db)
    zone = svc.get_zone(user=user, zone_id=zone_id)
    return success_response(_zone_dict(zone))


@router.post("")
def create_zone(
    req: ZoneCreate,
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = ZoneService(db)
    zone = svc.create_zone(user=user, req=req)
    return success_response(_zone_dict(zone))


@router.patch("/{zone_id}")
def update_zone(
    zone_id: UUID,
    req: ZoneUpdate,
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = ZoneService(db)
    zone = svc.update_zone(user=user, zone_id=zone_id, req=req)
    return success_response(_zone_dict(zone))
