from sqlalchemy import Column, String, Integer, text, TIMESTAMP, ForeignKey, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class LogisticItem(Base):
    __tablename__ = "logistic_items"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    quantity = Column(Integer, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class EventRequest(Base):
    __tablename__ = "event_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(255))
    catering_needed = Column(Boolean, server_default="FALSE")
    catering_details = Column(String)
    status = Column(String(50), server_default="Pending")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class LogisticItemRequest(Base):
    __tablename__ = "logistic_item_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    event_request_id = Column(UUID(as_uuid=True), ForeignKey("event_requests.id", ondelete="CASCADE"))
    item_id = Column(UUID(as_uuid=True), ForeignKey("logistic_items.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    status = Column(String(50), server_default="Pending")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
