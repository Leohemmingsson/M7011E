# std
import time

# own
from orm import User

# pip
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery(
    "user",
    broker="pyamqp://admin:mypass@host.docker.internal:5672//",
    backend="db+mysql://root:root@host.docker.internal:33066/celery",
)


@app.task(name="user.create_user")
def create_user(data: dict):
    logger.info("Got Request - Starting work ")
    new_user = User.add(**data)
    logger.info("Work Finished ")
    return new_user.to_dict
