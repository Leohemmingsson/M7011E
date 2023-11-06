class BaseConnection:
    def get_product_from_id(self, id):
        raise NotImplementedError

    def add_product(self, product):
        raise NotImplementedError

    def remove_product(self, id):
        raise NotImplementedError
