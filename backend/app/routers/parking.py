from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..auth import get_current_user, check_role
from ..models.maintenance import StaffVehicle
from ..models.user import User
from ..schemas.maintenance import StaffVehicleResponse, StaffVehicleCreate

router = APIRouter()

@router.get("/", response_model=List[StaffVehicleResponse])
def get_staff_vehicles(db: Session = Depends(get_db)):
    return db.query(StaffVehicle).all()

@router.post("/", response_model=StaffVehicleResponse)
def register_staff_vehicle(vehicle_in: StaffVehicleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if plate number exists
    existing_vehicle = db.query(StaffVehicle).filter(StaffVehicle.plate_number == vehicle_in.plate_number).first()
    if existing_vehicle:
        raise HTTPException(status_code=400, detail="Plate number already registered")
        
    new_vehicle = StaffVehicle(
        user_id=vehicle_in.user_id,
        plate_number=vehicle_in.plate_number,
        vehicle_model=vehicle_in.vehicle_model,
        color=vehicle_in.color,
        parking_lot_number=vehicle_in.parking_lot_number
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

@router.delete("/{vehicle_id}", dependencies=[Depends(check_role(["UPF Admin"]))])
def delete_staff_vehicle(vehicle_id: UUID, db: Session = Depends(get_db)):
    vehicle = db.query(StaffVehicle).filter(StaffVehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(vehicle)
    db.commit()
    return {"message": "Vehicle registry deleted"}
