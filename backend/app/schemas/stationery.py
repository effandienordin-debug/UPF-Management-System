from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class StationeryItemBase(BaseModel):
    item_name: str
    category: Optional[str] = None
    unit: Optional[str] = None
    stock_quantity: Optional[int] = 0
    minimum_stock_level: Optional[int] = 0
    storage_location: Optional[str] = None

class StationeryItemCreate(StationeryItemBase):
    pass

class StationeryItemResponse(StationeryItemBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionItemBase(BaseModel):
    item_id: UUID
    quantity: int

class StationeryTransactionCreate(BaseModel):
    staff_id: UUID
    department: str
    items: List[TransactionItemBase]

class StationeryTransactionResponse(BaseModel):
    id: UUID
    staff_id: Optional[UUID]
    issued_by: Optional[UUID]
    department: str
    transaction_date: datetime
    total_items: int

    class Config:
        orm_mode = True
