from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime, date

class VisitorBase(BaseModel):
    full_name: str
    ic_number: Optional[str] = None
    phone_number: Optional[str] = None
    company: Optional[str] = None
    purpose: Optional[str] = None
    visit_date: date
    host_id: Optional[UUID] = None

class VisitorCreate(VisitorBase):
    pass

class VisitorResponse(VisitorBase):
    id: UUID
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class VisitorPassBase(BaseModel):
    visitor_id: UUID
    pass_code: str
    expires_at: Optional[datetime] = None

class VisitorPassResponse(VisitorPassBase):
    id: UUID
    issued_at: datetime
    qr_code_path: Optional[str] = None

    class Config:
        orm_mode = True
