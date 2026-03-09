from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import relationship, declarative_base
from Backend.config import settings
from typing import AsyncGenerator
from sqlalchemy import UniqueConstraint

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class EventSlot(Base):
    __tablename__ = "event_slots"

    id = Column(Integer, primary_key=True)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    week = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    is_booked = Column(Boolean, default=False)

    bookings = relationship("Booking", back_populates="slot")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, nullable=False,unique=True,autoincrement=True)
    category_id = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    is_booked = Column(Boolean, nullable=False, default=False)
    bookings = relationship("Booking", back_populates="user")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False,autoincrement=True)
    slot_id = Column(Integer, ForeignKey("event_slots.id"), nullable=False)

    user = relationship("User", back_populates="bookings")
    slot = relationship("EventSlot", back_populates="bookings")

    __table_args__ = (
        UniqueConstraint("user_id", "slot_id", name="unique_user_slot_booking"),
    )
