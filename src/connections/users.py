# own
from data_types import User

# pip
from mysql.connector.cursor import MySQLCursor


def sql_get_user_from_pid(cursor: MySQLCursor, public_id: str) -> User:
    """
    Get user from id.
    """
    cursor.execute("SELECT * FROM User WHERE public_id = %s", (public_id,))
    result = cursor.fetchone()
    return User.from_list(result)


def sql_get_user_from_uname(cursor: MySQLCursor, uname: str) -> User:
    """
    Get user from name.
    """

    cursor.execute("SELECT * FROM User WHERE username = %s", (uname,))
    result = cursor.fetchone()
    return User.from_list(result)


def create_user(cursor: MySQLCursor, user: User) -> None:
    """
    Create user.
    """
    cursor.execute(
        "INSERT INTO User (public_id, username, password, first_name, last_name, mail, type) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (user.public_id, user.username, user.password, user.first_name, user.last_name, user.mail, user.type),
    )
