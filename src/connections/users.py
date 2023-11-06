# own
from data_types import User

# pip
from mysql.connector.cursor import MySQLCursor


def sql_get_user_from_pid(cursor: MySQLCursor, public_id: str) -> User:
    """
    Get user from id.
    """
    mock_user = _get_mock_user()
    return mock_user

    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    result = cursor.fetchone()
    return User(result)


def sql_get_user_from_uname(cursor: MySQLCursor, uname: str) -> User:
    """
    Get user from name.
    """

    mock_user = _get_mock_user()
    return mock_user

    cursor.execute("SELECT * FROM users WHERE username = %s", (uname,))
    result = cursor.fetchone()
    return User(result)


def _get_mock_user() -> User:
    return User(
        public_id="a9f7527b-7916-4726-a1f5-3068d6728411",
        username="test",
        password="9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        type="admin",
    )
