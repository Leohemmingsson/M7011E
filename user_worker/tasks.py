# std
import uuid

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

app.conf.task_routes = {
    "scheduler.create_user": {"queue": "user"},
    "scheduler.get_all_users": {"queue": "user"},
    "scheduler.get_user_by_username": {"queue": "user"},
    "scheduler.get_user_by_public_id": {"queue": "user"},
    "scheduler.activate_user_by_public_id": {"queue": "user"},
    "scheduler.delete_user_by_username": {"queue": "user"},
}

BaseModel.metadata.create_all(engine)


@app.task(queue="user", name="create_user")
def create_user(data: dict) -> tuple:
    data = data
    data["public_id"] = str(uuid.uuid4())
    data["activated"] = False
    new_user = User.add(**data)
    new_user.public_id  # The return is wrong if instance is not used
    new_user = new_user.to_dict

    return (new_user, 201)


@app.task(queue="user", name="get_all_users")
def get_all_users() -> tuple:
    users = User.get_all()
    all_users = [one_user.to_dict for one_user in users]
    return (all_users, 200)


@app.task(queue="user", name="get_user_by_username")
def get_user_by_username(username) -> tuple:
    statement = User.username == username
    user = User.get_first_where(statement)
    if user is None:
        return ("User not found", 404)

    return (user.to_dict, 200)


@app.task(queue="user", name="get_user_by_public_id")
def get_user_by_public_id(public_id) -> tuple:
    statement = User.public_id == public_id
    user = User.get_first_where(statement)
    if user is None:
        return ("User not found", 404)

    return (user.to_dict, 200)


@app.task(queue="user", name="activate_user_by_public_id")
def activate_user_by_public_id(public_id) -> tuple:
    statement = User.public_id == public_id
    user = User.get_first_where(statement)
    if user is None:
        return ("User not found", 404)

    user.update("activated", True)

    return ("User activated", 200)


@app.task(queue="user", name="delete_user_by_username")
def delete_user_by_username(username: str) -> tuple:
    statement = User.username == username
    User.delete_where(statement)
    return (f"User deleted: {username}", 200)
