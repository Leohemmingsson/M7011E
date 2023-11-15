# own
from shared_models import BaseModel

# pip
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship


class Order(BaseModel):
    __tablename__ = "Order"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(255))
    status = Column(Enum("in_progess", "done"))

    # relationships
    itemgroups = relationship("ItemGroup", back_populates="order")
