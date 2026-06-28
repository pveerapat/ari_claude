from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import list_response, success_response
from app.dependencies.auth import require_active_account, require_active_membership
from app.dependencies.db import get_db
from app.models.farm import Farm
from app.models.user import User
from app.schemas.farm import FarmCreate, FarmUpdate
from app.services.farm_service import FarmService

router = APIRouter(prefix="/farms", tags=["farms"])


def _farm_dict(farm: Farm) -> dict:
    return {
        "farm_id": str(farm.id),
        "organization_id": str(farm.organization_id),
        "farm_name": farm.name,
        "location": farm.location,
        "description": farm.description,
        "status": farm.status,
        "created_at": farm.created_at.isoformat() if farm.created_at else None,
        "updated_at": farm.updated_at.isoformat() if farm.updated_at else None,
    }


@router.get("")
def list_farms(
    organization_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
    q: Optional[str] = Query(None),
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = FarmService(db)
    farms, total = svc.list_farms(
        user=user,
        organization_id=organization_id,
        status=status,
        q=q,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return list_response([_farm_dict(f) for f in farms], page, page_size, total)


@router.get("/{farm_id}")
def get_farm(
    farm_id: UUID,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = FarmService(db)
    farm = svc.get_farm(user=user, farm_id=farm_id)
    return success_response(_farm_dict(farm))


@router.post("")
def create_farm(
    req: FarmCreate,
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = FarmService(db)
    farm = svc.create_farm(user=user, req=req)
    return success_response(_farm_dict(farm))


@router.patch("/{farm_id}")
def update_farm(
    farm_id: UUID,
    req: FarmUpdate,
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = FarmService(db)
    farm = svc.update_farm(user=user, farm_id=farm_id, req=req)
    return success_response(_farm_dict(farm))
