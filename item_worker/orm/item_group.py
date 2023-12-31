# own
from shared_models import BaseModel

# pip
from sqlalchemy import Column, Integer, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship


class ItemGroup(BaseModel):
    __tablename__ = "ItemGroup"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("Order.id"))
    item_id = Column(Integer, ForeignKey("Item.id"))
    quantity = Column(SmallInteger)

    # relationships
    item = relationship("Item", back_populates="itemgroups")
    order = relationship("Order", back_populates="itemgroups")
