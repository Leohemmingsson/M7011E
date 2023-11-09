from .authorization_levels import AuthorizationLevel
from orm import User


def is_authorized(
    user: User,
    required_permission: AuthorizationLevel | None = None,
    only_higher_than_user: bool = False,
    only_user: bool = False,
    allow_user_exeption: bool = False,
    exception_public_id: str | None = None,
    exception_username: str | None = None,
) -> bool:
    """
    Check if user is authorized to perform a given permission.
    Not activated users are not authorized, by default.
    Arguments:
      * user: User object of the user trying to access the resource
      * required_permission: AuthorizationLevel enum value of the required permission
      * only_higher_than_user: If True, the user will be authorized if he has a higher
        permission than the exception. But the user will habe access.
      * only_user: If True, the user will be authorized if he is the exception
      * allow_user_exeption: If True, the user will be authorized if he is the exception
        This means that a user with lower permission than the required permission will be
        authorized if he is the exception
      * exception_public_id: Public ID of the user that is the exception
      * exception_username: Username of the user that is the exception

    Returns:
        * True if the user is authorized
        * False if the user is not authorized
    """
    if user.activated is not True:
        return False

    if _is_superuser(user):
        return True

    if exception_public_id is not None and exception_username is not None:
        raise ValueError("Only one of exception_public_id and exception_username can be set")

    exception_user = None
    if exception_public_id is not None:
        exception_user = _get_user_from_public_id(exception_public_id)
    elif exception_username is not None:
        exception_user = _get_user_from_username(exception_username)

    if only_higher_than_user:
        if exception_user is None:
            raise ValueError("exception_public_id or exception_username must be set when only_higher_than_user is True")

        if str(exception_user.type) == AuthorizationLevel.SUPERUSER.name:
            required_permission = AuthorizationLevel.SUPERUSER
        else:
            print(f"{exception_user = }")
            required_permission = AuthorizationLevel(AuthorizationLevel[str(exception_user.type)].value + 1)

    if allow_user_exeption or only_user:
        if str(user.public_id) == exception_public_id or str(user.username) == exception_username:
            return True
        elif only_user:
            return False

    if _is_admin(user):
        if required_permission == AuthorizationLevel.SUPERUSER:
            return False
        return True

    if _is_customer(user):
        if required_permission != AuthorizationLevel.CUSTOMER:
            return False
        return True

    return False


def _get_user_from_public_id(public_id: str) -> User | None:
    statement = User.public_id == public_id
    user = User.get_first_where(statement)
    return user


def _get_user_from_username(username: str) -> User | None:
    statement = User.username == username
    user = User.get_first_where(statement)
    return user


def _is_superuser(user: User) -> bool:
    return str(user.type) == AuthorizationLevel.SUPERUSER.name


def _is_admin(user: User) -> bool:
    return str(user.type) == AuthorizationLevel.ADMIN.name


def _is_customer(user: User) -> bool:
    return str(user.type) == AuthorizationLevel.CUSTOMER.name
