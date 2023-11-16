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
    "scheduler.update_user_cloumns": {"queue": "user"},
    "scheduler.create_user_verification": {"queue": "user"},
    "scheduler.get_user_verification_by_public_id": {"queue": "user"},
    "scheduler.set_user_verification_attempts_zero": {"queue": "user"},
    "scheduler.create_item": {"queue": "item"},
    "scheduler.get_all_items": {"queue": "item"},
    "scheduler.get_item_by_id": {"queue": "item"},
    "scheduler.get_item_by_name": {"queue": "item"},
    "scheduler.delete_item_by_id": {"queue": "item"},
    "scheduler.delete_item_by_name": {"queue": "item"},
    "scheduler.update_item_fields": {"queue": "item"},
    "scheduler.create_order": {"queue": "item"},
    "scheduler.mark_order_done": {"queue": "item"},
    "scheduler.add_item_to_order": {"queue": "item"},
    "scheduler.remove_item_from_order": {"queue": "item"},
    "scheduler.get_all_orders": {"queue": "item"},
    "scheduler.get_order_by_id": {"queue": "item"},
    "scheduler.delete_order_by_id": {"queue": "item"},
    "scheduler.get_orders_by_customer_id": {"queue": "item"},
    "scheduler.get_uid_on_order": {"queue": "item"},
}
