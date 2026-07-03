from sqlalchemy import ForeignKey, String, Integer, Float, Date, JSON
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import date


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    maiden_name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    birth_date: Mapped[date] = mapped_column(Date)
    image: Mapped[str] = mapped_column(String)
    blood_group:Mapped[str] = mapped_column(String)
    height: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float)
    eye_color: Mapped[str] = mapped_column(String)
    hair: Mapped[dict] = mapped_column(JSON)
    ip: Mapped[str] = mapped_column(String)
    address: Mapped[dict] = mapped_column(JSON)
    country: Mapped[str] = mapped_column(String)
    mac_address: Mapped[str] = mapped_column(String)
    university: Mapped[str] = mapped_column(String)
    bank: Mapped[dict] = mapped_column(JSON)
    company: Mapped[dict] = mapped_column(JSON)
    ein: Mapped[str] = mapped_column(String)
    ssn: Mapped[str] = mapped_column(String)
    user_agent: Mapped[str] = mapped_column(String)
    crypto: Mapped[dict] = mapped_column(JSON)
    role: Mapped[str] = mapped_column(String)

    

class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True)
    todo: Mapped[str] = mapped_column(String)
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))