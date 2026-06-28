"""Simple scope guards for Farm Structure access (P2-6).

These are FastAPI dependency helpers used in conjunction with the existing
auth guards (require_active_account, require_active_membership).

Business-logic scope enforcement (org/farm hierarchy validation) lives in
the service layer, not here. These guards enforce structural access rules
that apply at the dependency level.
"""

from app.core.enums import FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.models.user import User

_PRIVILEGED_ROLES = {UserRole.admin, UserRole.root, UserRole.ari_staff}


def assert_active_membership(user: User) -> None:
    """Raise 403 if user's farm membership is not active."""
    if user.role not in _PRIVILEGED_ROLES and user.membership_status != MembershipStatus.active:
        raise AppError("membership_not_active", "Farm membership is not active", 403)


def assert_owner_write(user: User) -> None:
    """Raise 403 if user is not a farm owner (or privileged role).

    Used to block owner_family / farm_staff from creating Farm / Zone / Tree.
    """
    if user.role in _PRIVILEGED_ROLES:
        return
    if user.farmer_status != FarmerStatus.owner:
        raise AppError("farm_create_forbidden", "Only farm owners can perform this action", 403)
    if user.membership_status != MembershipStatus.active:
        raise AppError("membership_not_active", "Farm membership is not active", 403)
