from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Todos(Base):
    __tablename__="todos"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    complete=Column(Boolean, default=False)

    owner_id=Column(Integer, ForeignKey("users.id"))
    owner=relationship("Users", back_populates="todos")


class Users(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, unique=True,index=True)
    username=Column(String, unique=True,index=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password=Column(String)
    phone_number=Column(String, nullable=True)
    is_active=Column(Boolean, default=True)
    address_id=Column(Integer, ForeignKey("address.id"), nullable=True)

    todos=relationship("Todos",back_populates="owner")
    address=relationship("Address", back_populates="user_address")

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)

    user_address = relationship("Users", back_populates="address")
