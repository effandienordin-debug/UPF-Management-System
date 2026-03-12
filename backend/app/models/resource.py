from sqlalchemy import Column, String, Integer, text, TIMESTAMP, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String(255))
    resources = Column(ARRAY(String))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    plate_number = Column(String(20), unique=True, nullable=False)
    model = Column(String(100), nullable=False)
    type = Column(String(50))
    capacity = Column(Integer)
    status = Column(String(50), server_default="Available")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
