# own
from shared_models import BaseModel, db

# pip
from sqlalchemy import Column, String, Enum, Boolean, ForeignKey, Integer
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

    # New relationship to UserVerification
    user_verification = relationship("UserVerification", uselist=False, back_populates="user")

    # relationships
    orders = relationship("Order", back_populates="customer")
    address = relationship("Address", back_populates="users")

    @classmethod
    def add(cls, verification_info, *args, **kwargs):
        user = cls(*args, **kwargs)

        user.user_verification = verification_info

        db.session.add(verification_info)
        db.session.add(user)
        db.session.commit()
        return user
