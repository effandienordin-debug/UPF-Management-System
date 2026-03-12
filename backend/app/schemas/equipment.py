from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class EquipmentBase(BaseModel):
    name: str
    category: str
    serial_number: Optional[str] = None
    status: Optional[str] = "Available"
    condition: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentResponse(EquipmentBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class BorrowingBase(BaseModel):
    equipment_id: UUID
    expected_return_date: datetime
    purpose: Optional[str] = None

class BorrowingCreate(BorrowingBase):
    pass

class BorrowingResponse(BorrowingBase):
    id: UUID
    user_id: UUID
    borrow_date: datetime
    actual_return_date: Optional[datetime] = None
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
