# own
from shared_models import BaseModel

# pip
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship


class Order(BaseModel):
    __tablename__ = "Order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(255), nullable=False)
    status = Column(Enum("in_progress", "done"))

    # relationships
    itemgroups = relationship("ItemGroup", back_populates="order")
