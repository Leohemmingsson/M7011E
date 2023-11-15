# own
from shared_models import BaseModel

# pip
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship


class UserVerification(BaseModel):
    __tablename__ = "UserVerification"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_public_id = Column(String(255), ForeignKey("User.public_id"), unique=True, nullable=False)
    code = Column(String(255))
    timestamp = Column(DateTime)
    attempts = Column(Integer)

    # Relationship back to User
    user = relationship("User", back_populates="user_verification", uselist=False)
