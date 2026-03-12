from sqlalchemy import Column, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class StaffVehicle(Base):
    __tablename__ = "staff_vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    plate_number = Column(String(20), unique=True, nullable=False)
    vehicle_model = Column(String(100))
    color = Column(String(50))
    parking_lot_number = Column(String(20))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    description = Column(String)
    location = Column(String(255))
    priority = Column(String(50), server_default="Medium")
    status = Column(String(50), server_default="Open")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class TechnicianAssignment(Base):
    __tablename__ = "technician_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    maintenance_id = Column(UUID(as_uuid=True), ForeignKey("maintenance_requests.id", ondelete="CASCADE"))
    technician_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    status = Column(String(50), server_default="Assigned")
    assigned_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
