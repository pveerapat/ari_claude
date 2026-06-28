from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.tree import Tree
from app.models.zone import Zone
from app.repositories.base import BaseRepository


class TreeRepository(BaseRepository[Tree]):
    def __init__(self, db: Session) -> None:
        super().__init__(Tree, db)

    def get_by_id(self, tree_id: UUID) -> Tree | None:
        return self.db.query(Tree).filter(Tree.id == tree_id).first()

    def get_by_id_and_zone(self, tree_id: UUID, zone_id: UUID) -> Tree | None:
        return (
            self.db.query(Tree)
            .filter(Tree.id == tree_id, Tree.zone_id == zone_id)
            .first()
        )

    def list_by_zone(
        self,
        zone_id: UUID,
        status: Optional[str] = None,
        q: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Tree]:
        query = self.db.query(Tree).filter(Tree.zone_id == zone_id)
        if status:
            query = query.filter(Tree.status == status)
        if q:
            query = query.filter(Tree.tree_code.ilike(f"%{q}%"))
        col = getattr(Tree, sort_by, Tree.created_at)
        order = col.desc() if sort_order == "desc" else col.asc()
        return query.order_by(order).offset(offset).limit(limit).all()

    def count_by_zone(
        self, zone_id: UUID, status: Optional[str] = None, q: Optional[str] = None
    ) -> int:
        query = self.db.query(func.count(Tree.id)).filter(Tree.zone_id == zone_id)
        if status:
            query = query.filter(Tree.status == status)
        if q:
            query = query.filter(Tree.tree_code.ilike(f"%{q}%"))
        return query.scalar() or 0

    def list_by_farm(
        self,
        farm_id: UUID,
        status: Optional[str] = None,
        q: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Tree]:
        query = (
            self.db.query(Tree)
            .join(Zone, Tree.zone_id == Zone.id)
            .filter(Zone.farm_id == farm_id)
        )
        if status:
            query = query.filter(Tree.status == status)
        if q:
            query = query.filter(Tree.tree_code.ilike(f"%{q}%"))
        col = getattr(Tree, sort_by, Tree.created_at)
        order = col.desc() if sort_order == "desc" else col.asc()
        return query.order_by(order).offset(offset).limit(limit).all()

    def count_by_farm(
        self, farm_id: UUID, status: Optional[str] = None, q: Optional[str] = None
    ) -> int:
        query = (
            self.db.query(func.count(Tree.id))
            .join(Zone, Tree.zone_id == Zone.id)
            .filter(Zone.farm_id == farm_id)
        )
        if status:
            query = query.filter(Tree.status == status)
        if q:
            query = query.filter(Tree.tree_code.ilike(f"%{q}%"))
        return query.scalar() or 0

    def create(self, zone_id: UUID, tree_code: str, status: Optional[str] = None) -> Tree:
        tree = Tree(zone_id=zone_id, tree_code=tree_code, status=status or "active")
        self.db.add(tree)
        self.db.flush()
        return tree

    def update(self, tree: Tree, updates: dict) -> Tree:
        for key, value in updates.items():
            setattr(tree, key, value)
        self.db.flush()
        return tree
