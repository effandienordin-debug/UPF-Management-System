from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class MeetingBookingBase(BaseModel):
    room_id: UUID
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None

class MeetingBookingCreate(MeetingBookingBase):
    pass

class MeetingBookingResponse(MeetingBookingBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class VehicleBookingBase(BaseModel):
    vehicle_id: Optional[UUID] = None
    start_time: datetime
    end_time: datetime
    destination: str
    purpose: Optional[str] = None

class VehicleBookingCreate(VehicleBookingBase):
    pass

class VehicleBookingResponse(VehicleBookingBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class DriverAssignmentBase(BaseModel):
    booking_id: UUID
    driver_id: UUID

class DriverAssignmentResponse(DriverAssignmentBase):
    id: UUID
    status: str
    assigned_at: datetime

    class Config:
        orm_mode = True
