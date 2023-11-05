from .baseConnection import BaseConnection


class SqlHandler(BaseConnection):
    def get_product_from_id(self, id):
        ...

    def add_product(self, product):
        ...

    def remove_product(self, id):
        ...
