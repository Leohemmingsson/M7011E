# own
from shared_models import BaseModel

# pip
from sqlalchemy import Column, String, Enum, Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "User"

    public_id = Column(String(255), primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    password = Column(String(255))
    address_id = Column(Integer, ForeignKey("Address.id"))
    type = Column(Enum("CUSTOMER", "ADMIN", "SUPERUSER"))
    mail = Column(String(255))
    activated = Column(Boolean)
    verification_code = Column(String(255))
    verification_timestamp = Column(DateTime)
    verification_attempts = Column(Integer)

    # relationships
    orders = relationship("Order", back_populates="customer")
    address = relationship("Address", back_populates="users")
