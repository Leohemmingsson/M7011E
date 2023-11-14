# own
from shared_models import BaseModel, db

# pip
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship


class Order(BaseModel):
    __tablename__ = "Order"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(255), ForeignKey("User.public_id"))
    status = Column(Enum("in_progess", "done"))

    # relationships
    customer = relationship("User", back_populates="orders")
    itemgroups = relationship("ItemGroup", back_populates="order")

    @classmethod
    def add(cls, user, *args, **kwargs):
        order = cls(*args, **kwargs)

        user.orders.append(order)

        db.session.add(order)
        db.session.commit()
        return order
