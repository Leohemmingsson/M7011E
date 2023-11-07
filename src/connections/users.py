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


def sql_activate_user(cursor: MySQLCursor, public_id: str) -> None:
    """
    Activate user.
    """
    cursor.execute("UPDATE User SET activated = True WHERE public_id = %s", (public_id,))


def sql_delete_user_with_username(cursor: MySQLCursor, username: str) -> None:
    """
    Delete user.
    """
    cursor.execute("DELETE FROM User WHERE username = %s", (username,))


def sql_create_user(cursor: MySQLCursor, user: User) -> None:
    """
    Create user.
    """
    cursor.execute(
        "INSERT INTO User (public_id, username, password, first_name, last_name, mail, type, activated) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            user.public_id,
            user.username,
            user.password,
            user.first_name,
            user.last_name,
            user.mail,
            user.type,
            int(user.activated),
        ),
    )
