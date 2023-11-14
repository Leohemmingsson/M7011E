# own
from shared_model import BaseModel
from shared_model.base_model import engine

# pip
from celery import Celery
from celery.utils.log import get_task_logger
import time

logger = get_task_logger(__name__)

app = Celery(
    "item",
    broker="pyamqp://admin:mypass@host.docker.internal:5672//",
    backend="db+mysql://root:root@host.docker.internal:33066/celery",
)

app.conf.task_routes = {
    "scheduler.create_item": {"queue": "item"},
    "scheduler.get_all_items": {"queue": "item"},
    "scheduler.get_item_by_id": {"queue": "item"},
    "scheduler.delete_item_by_id": {"queue": "item"},
}


BaseModel.metadata.create_all(engine)


@app.task(queue="item", name="create_item")
def create_user(name):
    logger.info("Got Request - Starting work ")
    time.sleep(4)
    logger.info("Work Finished ")
    return f"{name} created"


@app.task(queue="item", name="get_all_items")
def get_all_items():
    ...


@app.task(queue="item", name="get_item_by_id")
def get_item_by_id(current_user, id):
    ...


@app.task(queue="item", name="delete_item_by_id")
def delete_item_by_id(current_user, id):
    ...
