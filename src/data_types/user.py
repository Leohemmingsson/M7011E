from dataclasses import dataclass


@dataclass
class User:
    public_id: str
    username: str
    password: str
    type: str
    first_name: str | None = None
    last_name: str | None = None
    mail: str | None = None
