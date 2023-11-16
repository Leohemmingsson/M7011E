# std
import uuid
import random
import datetime

# own
from orm import User, UserVerification
from shared_models import BaseModel, session
from shared_models.base_model import engine

# pip
from celery import Celery
from celery.utils.log import get_task_logger
from sqlalchemy.exc import IntegrityError

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
    "scheduler.update_user_cloumns": {"queue": "user"},
}

BaseModel.metadata.create_all(engine)


@app.task(queue="user", name="create_user")
def create_user(data: dict) -> tuple:
    try:
        data = data
        data["public_id"] = str(uuid.uuid4())
        data["activated"] = False

        verification_info = UserVerification()
        new_user = User.add(verification_info, **data)

        new_user.public_id  # The return is wrong if instance is not used
        new_user = new_user.to_dict

        return (new_user, 201)

    except IntegrityError:
        session.rollback()
        return ("user already exists", 409)


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


@app.task(queue="user", name="update_user_cloumns")
def update_user_cloumns(username: str, data) -> tuple:
    statement = User.username == username
    user = User.get_first_where(statement)

    for key, value in data.items():
        user.update(key, value)

    return (f"User updated: {username}", 200)


@app.task(queue="user", name="create_user_verification")
def create_user_verification(public_id: str) -> tuple:
    statement = UserVerification.id == public_id
    user_verification = UserVerification.get_first_where(statement)
    if user_verification is None:
        return ("Could not find user", 404)

    new_code = str(random.randint(100000, 999999))
    timestamp = datetime.datetime.utcnow()
    attempts = 3
    user_verification.update("code", new_code)
    user_verification.update("timestamp", timestamp)
    user_verification.update("attempts", attempts)

    return (f"User verification created: {public_id}", 200)


@app.task(queue="user", name="get_user_verification_by_public_id")
def get_user_verification_by_public_id(public_id):
    statement = UserVerification.id == public_id
    user_verification = UserVerification.get_first_where(statement)
    if user_verification is None:
        return ("Could not find user", 404)

    if int(user_verification.attempts) == 0:
        return ("No attempts left", 400)

    user_verification.update("attempts", user_verification.attempts - 1)

    return (user_verification.to_dict, 200)


@app.task(queue="user", name="set_user_verification_attemts_zero")
def set_user_verification_attemts_zero(public_id):
    statement = UserVerification.id == public_id
    user_verification = UserVerification.get_first_where(statement)

    if user_verification is None:
        return ("Could not find user", 404)

    user_verification.update("attempts", 0)
    return ("Attempts is set to 0", 200)
