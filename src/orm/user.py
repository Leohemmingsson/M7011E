# own
from shared_models import db

# pip
from sqlalchemy import Column, String, Enum, Boolean
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "User"

    public_id = Column(String(255), primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    password = Column(String(255), nullable=False)
    type = Column(Enum("customer", "admin", "superuser"))
    mail = Column(String(255), nullable=False)
    activated = Column(Boolean)

    # relationships
    orders = relationship("Order", back_populates="customer")
