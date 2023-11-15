# own
from shared_models import BaseModel, session
from shared_models.base_model import engine
from orm import Item

# pip
from celery import Celery
from celery.utils.log import get_task_logger
from sqlalchemy.exc import IntegrityError, OperationalError

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
    "scheduler.get_item_by_name": {"queue": "item"},
    "scheduler.delete_item_by_id": {"queue": "item"},
    "scheduler.delete_item_by_name": {"queue": "item"},
}


BaseModel.metadata.create_all(engine)


@app.task(queue="item", name="create_item")
def create_user(data: dict):
    try:
        new_item = Item.add(**data)
    except IntegrityError:
        session.rollback()
        return ("Item already exists", 400)
    except OperationalError as e:
        session.rollback()
        return (f"Error {e}", 400)

    return (f"Item: {new_item.name} created", 201)


@app.task(queue="item", name="get_all_items")
def get_all_items():
    all_items = Item.get_all()
    all_items = [one_item.to_dict for one_item in all_items]
    return (all_items, 200)


@app.task(queue="item", name="get_item_by_name")
def get_item_by_name(name):
    statement = Item.name == name
    item = Item.get_first_where(statement)
    if item is None:
        return ("Item not found", 404)

    return (item.to_dict, 200)


@app.task(queue="item", name="get_item_by_id")
def get_item_by_id(id):
    statement = Item.id == id
    item = Item.get_first_where(statement)
    if item is None:
        return ("Item not found", 404)

    return (item.to_dict, 200)


@app.task(queue="item", name="delete_item_by_id")
def delete_item_by_id(id):
    statement = Item.id == id
    Item.delete_where(statement)

    return (f"Item {id} deleted", 200)


@app.task(queue="item", name="delete_item_by_name")
def delete_item_by_name(name):
    statement = Item.name = name
    Item.delete_where(statement)

    return (f"Item {id} deleted", 200)


@app.task(queue="item", name="create_order")
def create_order(data: dict):
    raise NotImplementedError("Not implemented yet")


@app.task(queue="item", name="add_item_to_order")
def add_item_to_order(order_id: int, item_id: int, quantity: int):
    raise NotImplementedError("Not implemented yet")


@app.task(queue="item", name="remove_item_from_order")
def remove_item_from_order(order_id: int, item_id: int, quantity: int):
    raise NotImplementedError("Not implemented yet")


@app.task(queue="item", name="get_all_orders")
def get_all_orders():
    raise NotImplementedError("Not implemented yet")


@app.task(queue="item", name="get_order_by_id")
def get_order_by_id(id):
    raise NotImplementedError("Not implemented yet")


@app.task(queue="item", name="delete_order_by_id")
def delete_order_by_id(id):
    raise NotImplementedError("Not implemented yet")
