from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Date, ForeignKey, Table, Integer, String, Float
from typing import List
from datetime import date




class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


mechanic_service_ticket = db.Table(
    "mechanic_service_ticket",
    Base.metadata,
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"), primary_key=True),
    db.Column("service_ticket_id", db.ForeignKey("service_tickets.id"), primary_key=True)
)

#inventory and service ticket junction table 
inventory_service = db.Table(
    "inventory_service",
    Base.metadata,
    db.Column("inventory_id", db.ForeignKey("inventory.id"), primary_key=True),
    db.Column("service_ticket_id", db.ForeignKey("service_tickets.id"), primary_key=True)
)


class Customer(Base):
    __tablename__ = "customers"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)
    
    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship("ServiceTicket", back_populates="customer", cascade="all,delete")
    
class Mechanic(Base):
    __tablename__ = "mechanics"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(secondary=mechanic_service_ticket, back_populates="mechanics")

class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(50), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    service_description: Mapped[str] = mapped_column(db.String(500), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"), nullable=False)
    
    customer: Mapped["Customer"] = db.relationship("Customer", back_populates="service_tickets")
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary=mechanic_service_ticket, back_populates="service_tickets")
    inventory: Mapped[List["Inventory"]] = db.relationship(secondary=inventory_service, back_populates="service_tickets")

class Inventory(Base): #inventory model
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(db.Integer,unique=True, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(secondary=inventory_service, back_populates="inventory")