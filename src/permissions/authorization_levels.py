from enum import Enum


class AuthorizationLevel(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    SUPERUSER = "superuser"
