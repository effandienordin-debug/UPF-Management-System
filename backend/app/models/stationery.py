from sqlalchemy import Column, String, Integer, text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class StationeryItem(Base):
    __tablename__ = "stationery_items"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    item_name = Column(String(255), nullable=False)
    category = Column(String(255))
    unit = Column(String(50))
    stock_quantity = Column(Integer, server_default="0")
    minimum_stock_level = Column(Integer, server_default="0")
    storage_location = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class StationeryTransaction(Base):
    __tablename__ = "stationery_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    staff_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    issued_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    department = Column(String(255))
    transaction_date = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    total_items = Column(Integer, server_default="0")

class StationeryTransactionItem(Base):
    __tablename__ = "stationery_transaction_items"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("stationery_transactions.id", ondelete="CASCADE"))
    item_id = Column(UUID(as_uuid=True), ForeignKey("stationery_items.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
