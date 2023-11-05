from dataclasses import dataclass


@dataclass
class Item:
    id: int
    name: str
    in_stock: bool
    price: float
    img: str
