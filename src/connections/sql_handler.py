# std
import os

# pip
import mysql.connector


class SqlManager:
    """
    Context manager for SQL connections.
    Makes to load env variables, commit and close connection automatically.

    # Usage example:

    with SQLManager() as (cursor, mydb):
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        print(result)

    """

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=os.getenv("SQL_HOST"),
            user=os.getenv("SQL_USER"),
            port=os.getenv("SQL_PORT"),
            password=os.getenv("SQL_PASS"),
            database=os.getenv("SQL_DB"),
        )

    def __enter__(self):
        return (self.mydb.cursor(), self.mydb)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mydb.commit()
        self.mydb.close()


if __name__ == "__main__":
    with SqlManager() as (cursor, mydb):
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        print(result)
