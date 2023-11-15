# pip
from celery import Celery

celery_obj = Celery(
    "scheduler",
    broker="pyamqp://admin:mypass@host.docker.internal:5672//",
    backend="db+mysql://root:root@host.docker.internal:33066/celery",
)


celery_obj.conf.task_routes = {
    "scheduler.create_user": {"queue": "user"},
    "scheduler.get_all_users": {"queue": "user"},
    "scheduler.get_user_by_username": {"queue": "user"},
    "scheduler.get_user_by_public_id": {"queue": "user"},
    "scheduler.activate_user_by_public_id": {"queue": "user"},
    "scheduler.delete_user_by_username": {"queue": "user"},
    "scheduler.create_item": {"queue": "item"},
    "scheduler.get_all_items": {"queue": "item"},
    "scheduler.get_item_by_id": {"queue": "item"},
    "scheduler.get_item_by_name": {"queue": "item"},
    "scheduler.delete_item_by_id": {"queue": "item"},
    "scheduler.delete_item_by_name": {"queue": "item"},
}
