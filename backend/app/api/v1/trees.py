from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import list_response, success_response
from app.dependencies.auth import require_active_account, require_active_membership
from app.dependencies.db import get_db
from app.models.tree import Tree
from app.models.user import User
from app.schemas.tree import TreeCreate, TreeUpdate
from app.services.tree_service import TreeService

router = APIRouter(prefix="/trees", tags=["trees"])


def _tree_dict(tree: Tree) -> dict:
    return {
        "tree_id": str(tree.id),
        "zone_id": str(tree.zone_id),
        "tree_code": tree.tree_code,
        "status": tree.status,
        "created_at": tree.created_at.isoformat() if tree.created_at else None,
        "updated_at": tree.updated_at.isoformat() if tree.updated_at else None,
    }


@router.get("")
def list_trees(
    zone_id: Optional[UUID] = Query(None),
    farm_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
    q: Optional[str] = Query(None),
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = TreeService(db)
    trees, total = svc.list_trees(
        user=user,
        zone_id=zone_id,
        farm_id=farm_id,
        status=status,
        q=q,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return list_response([_tree_dict(t) for t in trees], page, page_size, total)


@router.get("/{tree_id}")
def get_tree(
    tree_id: UUID,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = TreeService(db)
    tree = svc.get_tree(user=user, tree_id=tree_id)
    return success_response(_tree_dict(tree))


@router.post("")
def create_tree(
    req: TreeCreate,
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = TreeService(db)
    tree = svc.create_tree(user=user, req=req)
    return success_response(_tree_dict(tree))


@router.patch("/{tree_id}")
def update_tree(
    tree_id: UUID,
    req: TreeUpdate,
    user: User = Depends(require_active_account),
    db: Session = Depends(get_db),
):
    svc = TreeService(db)
    tree = svc.update_tree(user=user, tree_id=tree_id, req=req)
    return success_response(_tree_dict(tree))
