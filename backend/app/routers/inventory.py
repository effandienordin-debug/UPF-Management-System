from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..auth import get_current_user, check_role
from ..models.logistic import LogisticItem, EventRequest, LogisticItemRequest
from ..models.user import User
from ..schemas.logistic import LogisticItemResponse, LogisticItemCreate, EventRequestResponse, EventRequestCreate

router = APIRouter()

@router.get("/items", response_model=List[LogisticItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(LogisticItem).all()

@router.post("/items", response_model=LogisticItemResponse, dependencies=[Depends(check_role(["UPF Admin"]))])
def create_item(item_in: LogisticItemCreate, db: Session = Depends(get_db)):
    new_item = LogisticItem(**item_in.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/events", response_model=List[EventRequestResponse])
def get_event_requests(db: Session = Depends(get_db)):
    return db.query(EventRequest).all()

@router.post("/events", response_model=EventRequestResponse)
def create_event_request(request_in: EventRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_request = EventRequest(
        user_id=current_user.id,
        title=request_in.title,
        date=request_in.date,
        location=request_in.location,
        catering_needed=request_in.catering_needed,
        catering_details=request_in.catering_details,
        status='Pending'
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    # Add items
    for item in request_in.items:
        new_item_request = LogisticItemRequest(
            event_request_id=new_request.id,
            item_id=item["item_id"],
            quantity=item["quantity"],
            status='Pending'
        )
        db.add(new_item_request)
    
    db.commit()
    db.refresh(new_request)
    return new_request
