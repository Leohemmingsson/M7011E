import os


def get_mysql_uri():
    """
    Get the mysql uri with the environment variables, all loaded from env
    """
    USERNAME = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASS")
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    DATABASE = os.getenv("DB_DATABASE")

    return f"mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
