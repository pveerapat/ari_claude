from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.farm import Farm
from app.repositories.base import BaseRepository


class FarmRepository(BaseRepository[Farm]):
    def __init__(self, db: Session) -> None:
        super().__init__(Farm, db)

    def get_by_id(self, farm_id: UUID) -> Farm | None:
        return self.db.query(Farm).filter(Farm.id == farm_id).first()

    def get_by_id_and_org(self, farm_id: UUID, organization_id: UUID) -> Farm | None:
        return (
            self.db.query(Farm)
            .filter(Farm.id == farm_id, Farm.organization_id == organization_id)
            .first()
        )

    def list_by_org(
        self,
        organization_id: UUID,
        status: Optional[str] = None,
        q: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Farm]:
        query = self.db.query(Farm).filter(Farm.organization_id == organization_id)
        if status:
            query = query.filter(Farm.status == status)
        if q:
            query = query.filter(Farm.name.ilike(f"%{q}%"))
        col = getattr(Farm, sort_by, Farm.created_at)
        order = col.desc() if sort_order == "desc" else col.asc()
        return query.order_by(order).offset(offset).limit(limit).all()

    def count_by_org(
        self,
        organization_id: UUID,
        status: Optional[str] = None,
        q: Optional[str] = None,
    ) -> int:
        query = self.db.query(func.count(Farm.id)).filter(Farm.organization_id == organization_id)
        if status:
            query = query.filter(Farm.status == status)
        if q:
            query = query.filter(Farm.name.ilike(f"%{q}%"))
        return query.scalar() or 0

    def create(
        self,
        organization_id: UUID,
        name: str,
        location: Optional[dict] = None,
        description: Optional[str] = None,
    ) -> Farm:
        farm = Farm(
            organization_id=organization_id,
            name=name,
            location=location,
            description=description,
            status="active",
        )
        self.db.add(farm)
        self.db.flush()
        return farm

    def update(self, farm: Farm, updates: dict) -> Farm:
        for key, value in updates.items():
            setattr(farm, key, value)
        self.db.flush()
        return farm
