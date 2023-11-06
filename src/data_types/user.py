class User:
    def __init__(self, public_id, username, password, first_name=None, last_name=None, mail=None, type="customer"):
        self.public_id: str = public_id
        self.username: str = username
        self.password: str = password
        self.type: str = type
        self.first_name: str | None = first_name
        self.last_name: str | None = last_name
        self.mail: str | None = mail

    @classmethod
    def from_list(cls, data: list) -> "User":
        values = {
            "public_id": data[0],
            "username": data[1],
            "first_name": data[2],
            "last_name": data[3],
            "password": data[4],
            "type": data[5],
            "mail": data[6],
        }
        return cls(**values)
