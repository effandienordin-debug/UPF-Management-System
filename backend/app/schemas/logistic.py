from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date

class LogisticItemBase(BaseModel):
    name: str
    category: Optional[str] = None
    quantity: Optional[int] = 0

class LogisticItemCreate(LogisticItemBase):
    pass

class LogisticItemResponse(LogisticItemBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class EventRequestBase(BaseModel):
    title: str
    date: date
    location: Optional[str] = None
    catering_needed: Optional[bool] = False
    catering_details: Optional[str] = None

class EventRequestCreate(EventRequestBase):
    items: List[dict] # [{item_id: UUID, quantity: int}]

class EventRequestResponse(EventRequestBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class LogisticItemRequestBase(BaseModel):
    event_request_id: UUID
    item_id: UUID
    quantity: int

class LogisticItemRequestResponse(LogisticItemRequestBase):
    id: UUID
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
