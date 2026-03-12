from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class StaffVehicleBase(BaseModel):
    plate_number: str
    vehicle_model: Optional[str] = None
    color: Optional[str] = None
    parking_lot_number: Optional[str] = None

class StaffVehicleCreate(StaffVehicleBase):
    user_id: UUID

class StaffVehicleResponse(StaffVehicleBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class MaintenanceRequestBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    priority: Optional[str] = "Medium"

class MaintenanceRequestCreate(MaintenanceRequestBase):
    pass

class MaintenanceRequestResponse(MaintenanceRequestBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class TechnicianAssignmentBase(BaseModel):
    maintenance_id: UUID
    technician_id: UUID

class TechnicianAssignmentResponse(TechnicianAssignmentBase):
    id: UUID
    status: str
    assigned_at: datetime

    class Config:
        orm_mode = True
