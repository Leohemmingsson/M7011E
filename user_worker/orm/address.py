# own
from shared_models import BaseModel

# pip
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Address(BaseModel):
    __tablename__ = "Address"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)

    users = relationship("User", back_populates="address")
