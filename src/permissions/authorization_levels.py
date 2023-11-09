from enum import Enum


class AuthorizationLevel(Enum):
    CUSTOMER = 0
    ADMIN = 1
    SUPERUSER = 2
