from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.core.enums import AccountStatus, MembershipStatus
from app.dependencies.db import get_db
from app.models.user import User
from app.repositories.auth import AuthRepository

_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token subject")

    user = AuthRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_authenticated_user(user: User = Depends(get_current_user)) -> User:
    return user


def require_active_account(user: User = Depends(get_current_user)) -> User:
    _ACTIVE = {AccountStatus.active, AccountStatus.active_pending_verification}
    if user.account_status not in _ACTIVE:
        raise HTTPException(status_code=403, detail="Account is not active")
    return user


def require_active_membership(user: User = Depends(require_active_account)) -> User:
    if user.membership_status != MembershipStatus.active:
        raise HTTPException(status_code=403, detail="Farm membership is not active")
    return user
