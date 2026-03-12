from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class RoomBase(BaseModel):
    name: str
    capacity: int
    location: Optional[str] = None
    resources: Optional[List[str]] = None

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class VehicleBase(BaseModel):
    plate_number: str
    model: str
    type: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = "Available"

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
