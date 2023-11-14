# std
import time

# own
from orm import User
from shared_models import BaseModel
from shared_models.base_model import engine

# pip
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery(
    "user",
    broker="pyamqp://admin:mypass@host.docker.internal:5672//",
    backend="db+mysql://root:root@host.docker.internal:33066/celery",
)

BaseModel.metadata.create_all(engine)


@app.task(name="user.create_user")
def create_user(data: dict):
    new_user = User.add(**data)
    return new_user.to_dict


@app.task(name="user.get_all_users")
def get_all_users() -> list:
    users = User.get_all()
    all_users = [one_user.to_dict for one_user in users]
    return all_users


@app.task(name="user.delete_user")
def delete_user(username: str):
    statement = User.username == username
    User.delete_where(statement)
    return f"User deleted: {username}"
