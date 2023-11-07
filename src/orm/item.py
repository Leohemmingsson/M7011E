# own
from .base_class import BaseModel

# pip
from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship


class Item(BaseModel):
    __tablename__ = "Item"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    in_stock = Column(SmallInteger)
    price = Column(Integer)
    img = Column(String(255))

    # relationships
    itemgroups = relationship("ItemGroup", back_populates="item")
