from sqlalchemy import Column, String, text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True)
    status = Column(String(50), server_default="Available")
    condition = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class EquipmentBorrowing(Base):
    __tablename__ = "equipment_borrowing"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    equipment_id = Column(UUID(as_uuid=True), ForeignKey("equipment.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    borrow_date = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    expected_return_date = Column(TIMESTAMP(timezone=True), nullable=False)
    actual_return_date = Column(TIMESTAMP(timezone=True))
    purpose = Column(String)
    status = Column(String(50), server_default="Borrowed")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
