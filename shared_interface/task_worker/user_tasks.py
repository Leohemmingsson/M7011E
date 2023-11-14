from .scheduler_creater import celery_obj


@celery_obj.task(queue="user", name="create_user")
def create_user(data: dict) -> tuple:
    ...


@celery_obj.task(queue="user", name="get_all_users")
def get_all_users() -> tuple:
    ...


@celery_obj.task(queue="user", name="get_user_by_username")
def get_user_by_username(username) -> tuple:
    ...


@celery_obj.task(queue="user", name="get_user_by_public_id")
def get_user_by_public_id(public_id) -> tuple:
    ...


@celery_obj.task(queue="user", name="activate_user_by_public_id")
def activate_user_by_public_id(public_id) -> tuple:
    ...


@celery_obj.task(queue="user", name="delete_user_by_username")
def delete_user_by_username(username: str) -> tuple:
    ...
