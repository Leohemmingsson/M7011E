from celery import Celery
from celery.utils.log import get_task_logger
import time

logger = get_task_logger(__name__)

app = Celery(
    "item",
    broker="pyamqp://admin:mypass@host.docker.internal:5672//",
    backend="db+mysql://root:root@host.docker.internal:33066/celery",
)


@app.task(name="item.create_item")
def create_user(name):
    logger.info("Got Request - Starting work ")
    time.sleep(4)
    logger.info("Work Finished ")
    return f"{name} created"
