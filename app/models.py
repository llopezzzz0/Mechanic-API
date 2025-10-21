from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Date, ForeignKey, Table, Integer, String, Float




db = SQLAlchemy()



class Base(DeclarativeBase):
    pass


mechanic_service_ticket = Table(
    "mechanic_service_ticket",
    Base.metadata,
    Column("mechanic_id", ForeignKey("mechanics.id"), primary_key=True),
    Column("service_ticket_id", ForeignKey("service_tickets.id"), primary_key=True)
)


class Customer(Base):
    __tablename__ = "customers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    
class Mechanic(Base):
    __tablename__ = "mechanics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    service_tickets: Mapped[list["ServiceTicket"]] = relationship(secondary=mechanic_service_ticket, back_populates="mechanics")

class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vin: Mapped[str] = mapped_column(String(50), nullable=False)
    date: Mapped[str] = mapped_column(Date, nullable=False)
    service_description: Mapped[str] = mapped_column(String(500), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    mechanics: Mapped[list["Mechanic"]] = relationship(secondary=mechanic_service_ticket, back_populates="service_tickets")