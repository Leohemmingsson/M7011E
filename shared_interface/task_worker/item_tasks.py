from .scheduler_creater import celery_obj


@celery_obj.task(queue="item", name="create_item")
def create_item(name: str):
    ...


@celery_obj.task(queue="item", name="get_all_items")
def get_all_items():
    ...


@celery_obj.task(queue="item", name="get_item_by_id")
def get_item_by_id(current_user, id):
    ...


@celery_obj.task(queue="item", name="delete_item_by_id")
def delete_item_by_id(current_user, id):
    ...
