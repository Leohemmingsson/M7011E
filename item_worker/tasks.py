# own
from shared_models import BaseModel, session
from shared_models.base_model import engine
from orm import Item, Order, ItemGroup

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
    "scheduler.create_order": {"queue": "item"},
    "scheduler.mark_order_done": {"queue": "item"},
    "scheduler.add_item_to_order": {"queue": "item"},
    "scheduler.remove_item_from_order": {"queue": "item"},
    "scheduler.get_all_orders": {"queue": "item"},
    "scheduler.get_order_by_id": {"queue": "item"},
    "scheduler.delete_order_by_id": {"queue": "item"},
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
    Order.add(**data)
    return ("Order created", 201)


@app.task(queue="item", name="mark_order_done")
def mark_order_done(order_id: int):
    statement = Order.id == order_id
    order = Order.get_first_where(statement)
    if order is None:
        return ("Order not found", 404)
    order.update("status", "done")

    return ("Order marked as done", 200)


@app.task(queue="item", name="add_item_to_order")
def add_item_to_order(order_id: int, item_id: int, quantity: int):
    arguments = {"order_id": order_id, "item_id": item_id, "quantity": quantity}
    ItemGroup.add(**arguments)
    return ("Item added to order", 200)


@app.task(queue="item", name="remove_item_from_order")
def remove_item_from_order(order_id: int, item_id: int, quantity: int):
    statement = ItemGroup.order_id == order_id
    statement2 = ItemGroup.item_id == item_id
    item_group = ItemGroup.get_first_where(statement, statement2)
    if item_group is None:
        return ("Item not found in order", 404)

    if int(item_group.quantity) > quantity:
        item_group.update("quantity", int(item_group.quantity) - quantity)
        return ("Item quantity updated", 200)
    else:
        ItemGroup.delete_where(statement, statement2)
        return ("Item removed from order", 200)


@app.task(queue="item", name="get_all_orders")
def get_all_orders():
    all_orders = Order.get_all()
    all_orders = [one_order.to_dict for one_order in all_orders]
    return (all_orders, 200)


@app.task(queue="item", name="get_order_by_id")
def get_order_by_id(id):
    statement = Order.id == id
    order = Order.get_first_where(statement)

    if order is None:
        return ("Order not found", 404)

    return (order.to_dict, 200)


@app.task(queue="item", name="delete_order_by_id")
def delete_order_by_id(id):
    statement = Order.id == id
    Order.delete_where(statement)
    return ("Order deleted", 200)
