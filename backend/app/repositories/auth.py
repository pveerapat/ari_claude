from uuid import UUID

from sqlalchemy.orm import Session

from app.models.farm import Farm
from app.models.organization import Organization
from app.models.user import User
from app.repositories.base import BaseRepository


class AuthRepository(BaseRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(User, db)

    def get_by_phone(self, phone: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.phone == phone, User.deleted_at.is_(None))
            .first()
        )

    def get_by_id(self, user_id: UUID) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id, User.deleted_at.is_(None))
            .first()
        )

    def get_farm_by_id(self, farm_id: UUID) -> Farm | None:
        return self.db.query(Farm).filter(Farm.id == farm_id).first()

    def create_organization(self, name: str) -> Organization:
        org = Organization(name=name, type="individual", status="active")
        self.db.add(org)
        self.db.flush()
        return org

    def create_user(self, **kwargs) -> User:
        user = User(**kwargs)
        self.db.add(user)
        self.db.flush()
        return user
