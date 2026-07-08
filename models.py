from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # Admin, Support Agent, Customer

    tickets = relationship("Ticket", back_populates="agent")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)

    tickets = relationship("Ticket", back_populates="customer")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    assigned_agent_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(String)
    category = Column(String)
    status = Column(String, default="Open")

    customer = relationship("Customer", back_populates="tickets")
    agent = relationship("User", back_populates="tickets")