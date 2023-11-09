from .authorization_levels import AuthorizationLevel
from orm import User


def is_authorized(user: User, required_permission: AuthorizationLevel, user_public_id: str | None = None) -> bool:
    """Check if user is authorized to perform a given permission."""
    if user.activated is False:
        return False

    if _is_superuser(user):
        return True

    if _is_admin(user):
        if required_permission == AuthorizationLevel.SUPERUSER:
            return False
        return True

    if _is_customer(user):
        if required_permission != AuthorizationLevel.CUSTOMER:
            return False
        return True

    return False


def _is_superuser(user: User) -> bool:
    return str(user.type) == AuthorizationLevel.SUPERUSER.value


def _is_admin(user: User) -> bool:
    return str(user.type) == AuthorizationLevel.ADMIN.value


def _is_customer(user: User) -> bool:
    return str(user.type) == AuthorizationLevel.CUSTOMER.value
