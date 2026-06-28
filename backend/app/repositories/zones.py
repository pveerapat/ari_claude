from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.zone import Zone
from app.repositories.base import BaseRepository


class ZoneRepository(BaseRepository[Zone]):
    def __init__(self, db: Session) -> None:
        super().__init__(Zone, db)

    def get_by_id(self, zone_id: UUID) -> Zone | None:
        return self.db.query(Zone).filter(Zone.id == zone_id).first()

    def get_by_id_and_farm(self, zone_id: UUID, farm_id: UUID) -> Zone | None:
        return (
            self.db.query(Zone)
            .filter(Zone.id == zone_id, Zone.farm_id == farm_id)
            .first()
        )

    def list_by_farm(
        self,
        farm_id: UUID,
        q: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Zone]:
        query = self.db.query(Zone).filter(Zone.farm_id == farm_id)
        if q:
            query = query.filter(Zone.name.ilike(f"%{q}%"))
        col = getattr(Zone, sort_by, Zone.created_at)
        order = col.desc() if sort_order == "desc" else col.asc()
        return query.order_by(order).offset(offset).limit(limit).all()

    def count_by_farm(self, farm_id: UUID, q: Optional[str] = None) -> int:
        query = self.db.query(func.count(Zone.id)).filter(Zone.farm_id == farm_id)
        if q:
            query = query.filter(Zone.name.ilike(f"%{q}%"))
        return query.scalar() or 0

    def list_by_org_farms(
        self,
        farm_ids: list[UUID],
        q: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Zone]:
        if not farm_ids:
            return []
        query = self.db.query(Zone).filter(Zone.farm_id.in_(farm_ids))
        if q:
            query = query.filter(Zone.name.ilike(f"%{q}%"))
        col = getattr(Zone, sort_by, Zone.created_at)
        order = col.desc() if sort_order == "desc" else col.asc()
        return query.order_by(order).offset(offset).limit(limit).all()

    def count_by_org_farms(self, farm_ids: list[UUID], q: Optional[str] = None) -> int:
        if not farm_ids:
            return 0
        query = self.db.query(func.count(Zone.id)).filter(Zone.farm_id.in_(farm_ids))
        if q:
            query = query.filter(Zone.name.ilike(f"%{q}%"))
        return query.scalar() or 0

    def create(self, farm_id: UUID, name: str, description: Optional[str] = None) -> Zone:
        zone = Zone(farm_id=farm_id, name=name, description=description)
        self.db.add(zone)
        self.db.flush()
        return zone

    def update(self, zone: Zone, updates: dict) -> Zone:
        for key, value in updates.items():
            setattr(zone, key, value)
        self.db.flush()
        return zone
