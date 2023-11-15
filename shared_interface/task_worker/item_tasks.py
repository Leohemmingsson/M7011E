from .scheduler_creater import celery_obj


@celery_obj.task(queue="item", name="create_item")
def create_item(name: str):
    ...


@celery_obj.task(queue="item", name="get_all_items")
def get_all_items():
    ...


@celery_obj.task(queue="item", name="get_item_by_id")
def get_item_by_id(id):
    ...


@celery_obj.task(queue="item", name="get_item_by_name")
def get_item_by_name(name):
    ...


@celery_obj.task(queue="item", name="delete_item_by_id")
def delete_item_by_id(id):
    ...


@celery_obj.task(queue="item", name="delete_item_by_name")
def delete_item_by_name(name):
    ...


@celery_obj.task(queue="item", name="create_order")
def create_order(data: dict):
    ...


@celery_obj.task(queue="item", name="mark_order_done")
def mark_order_done(order_id: int):
    ...


@celery_obj.task(queue="item", name="add_item_to_order")
def add_item_to_order(order_id: int, item_id: int, quantity: int):
    ...


@celery_obj.task(queue="item", name="remove_item_from_order")
def remove_item_from_order(order_id: int, item_id: int, quantity: int):
    ...


@celery_obj.task(queue="item", name="get_all_orders")
def get_all_orders():
    ...


@celery_obj.task(queue="item", name="get_order_by_id")
def get_order_by_id(id):
    ...


@celery_obj.task(queue="item", name="delete_order_by_id")
def delete_order_by_id(id):
    ...
