from sqlalchemy import Column, String, TIMESTAMP, text, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class MeetingBooking(Base):
    __tablename__ = "meeting_bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    purpose = Column(String)
    status = Column(String(50), server_default="Pending")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class VehicleBooking(Base):
    __tablename__ = "vehicle_bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id", ondelete="SET NULL"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    destination = Column(String, nullable=False)
    purpose = Column(String)
    status = Column(String(50), server_default="Pending")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class DriverAssignment(Base):
    __tablename__ = "driver_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    booking_id = Column(UUID(as_uuid=True), ForeignKey("vehicle_bookings.id", ondelete="CASCADE"))
    driver_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    status = Column(String(50), server_default="Assigned")
    assigned_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
