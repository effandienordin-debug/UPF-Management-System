from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..auth import get_current_user, check_role
from ..models.resource import Room
from ..models.booking import MeetingBooking
from ..models.user import User
from ..schemas.resource import RoomResponse, RoomCreate
from ..schemas.booking import MeetingBookingResponse, MeetingBookingCreate

router = APIRouter()

@router.get("/rooms", response_model=List[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

@router.post("/rooms", response_model=RoomResponse, dependencies=[Depends(check_role(["UPF Admin"]))])
def create_room(room_in: RoomCreate, db: Session = Depends(get_db)):
    new_room = Room(**room_in.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("/bookings", response_model=List[MeetingBookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(MeetingBooking).all()

@router.post("/bookings", response_model=MeetingBookingResponse)
def create_booking(booking_in: MeetingBookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Basic conflict detection (simple example)
    existing_booking = db.query(MeetingBooking).filter(
        MeetingBooking.room_id == booking_in.room_id,
        MeetingBooking.status != 'Cancelled',
        MeetingBooking.start_time < booking_in.end_time,
        MeetingBooking.end_time > booking_in.start_time
    ).first()
    
    if existing_booking:
        raise HTTPException(status_code=400, detail="Room is already booked for this time slot")

    new_booking = MeetingBooking(
        **booking_in.dict(),
        user_id=current_user.id,
        status='Pending'
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.patch("/bookings/{booking_id}/status", dependencies=[Depends(check_role(["UPF Admin"]))])
def update_booking_status(booking_id: UUID, status: str, db: Session = Depends(get_db)):
    booking = db.query(MeetingBooking).filter(MeetingBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = status
    db.commit()
    return {"message": f"Booking status updated to {status}"}
