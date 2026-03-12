from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..auth import get_current_user, check_role
from ..models.resource import Vehicle
from ..models.booking import VehicleBooking, DriverAssignment
from ..models.user import User
from ..schemas.resource import VehicleResponse, VehicleCreate
from ..schemas.booking import VehicleBookingResponse, VehicleBookingCreate, DriverAssignmentResponse

router = APIRouter()

@router.get("/", response_model=List[VehicleResponse])
def get_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()

@router.post("/", response_model=VehicleResponse, dependencies=[Depends(check_role(["UPF Admin"]))])
def create_vehicle(vehicle_in: VehicleCreate, db: Session = Depends(get_db)):
    new_vehicle = Vehicle(**vehicle_in.dict())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

@router.get("/bookings", response_model=List[VehicleBookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(VehicleBooking).all()

@router.post("/bookings", response_model=VehicleBookingResponse)
def create_booking(booking_in: VehicleBookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Simple conflict detection
    if booking_in.vehicle_id:
        existing_booking = db.query(VehicleBooking).filter(
            VehicleBooking.vehicle_id == booking_in.vehicle_id,
            VehicleBooking.status != 'Cancelled',
            VehicleBooking.start_time < booking_in.end_time,
            VehicleBooking.end_time > booking_in.start_time
        ).first()
        if existing_booking:
            raise HTTPException(status_code=400, detail="Vehicle is already booked for this time slot")

    new_booking = VehicleBooking(
        **booking_in.dict(),
        user_id=current_user.id,
        status='Pending'
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.post("/assign-driver", response_model=DriverAssignmentResponse, dependencies=[Depends(check_role(["UPF Admin"]))])
def assign_driver(assignment_in: dict, db: Session = Depends(get_db)):
    new_assignment = DriverAssignment(
        booking_id=assignment_in["booking_id"],
        driver_id=assignment_in["driver_id"],
        status='Assigned'
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment
