from sqlalchemy import Column, String, TIMESTAMP, text, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    full_name = Column(String(255), nullable=False)
    ic_number = Column(String(20))
    phone_number = Column(String(20))
    company = Column(String(255))
    purpose = Column(String)
    visit_date = Column(Date, nullable=False)
    host_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    status = Column(String(50), server_default="Registered")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class VisitorPass(Base):
    __tablename__ = "visitor_pass"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitors.id", ondelete="CASCADE"))
    pass_code = Column(String(100), unique=True, nullable=False)
    issued_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    expires_at = Column(TIMESTAMP(timezone=True))
    qr_code_path = Column(String)
