from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime
from ..database import get_db
from ..auth import get_current_user, check_role
from ..models.equipment import Equipment, EquipmentBorrowing
from ..models.user import User
from ..schemas.equipment import EquipmentResponse, EquipmentCreate, BorrowingResponse, BorrowingCreate

router = APIRouter()

@router.get("/", response_model=List[EquipmentResponse])
def get_equipment(db: Session = Depends(get_db)):
    return db.query(Equipment).all()

@router.post("/", response_model=EquipmentResponse, dependencies=[Depends(check_role(["UPF Admin"]))])
def create_equipment(equipment_in: EquipmentCreate, db: Session = Depends(get_db)):
    new_equipment = Equipment(**equipment_in.dict())
    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)
    return new_equipment

@router.post("/borrow", response_model=BorrowingResponse)
def borrow_equipment(borrow_in: BorrowingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check equipment availability
    equipment = db.query(Equipment).filter(Equipment.id == borrow_in.equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    if equipment.status != 'Available':
        raise HTTPException(status_code=400, detail="Equipment is not available for borrowing")

    # Create borrowing record
    new_borrowing = EquipmentBorrowing(
        equipment_id=borrow_in.equipment_id,
        user_id=current_user.id,
        expected_return_date=borrow_in.expected_return_date,
        purpose=borrow_in.purpose,
        status='Borrowed'
    )
    
    # Update equipment status
    equipment.status = 'Borrowed'
    
    db.add(new_borrowing)
    db.commit()
    db.refresh(new_borrowing)
    return new_borrowing

@router.post("/return/{borrowing_id}")
def return_equipment(borrowing_id: UUID, db: Session = Depends(get_db)):
    borrowing = db.query(EquipmentBorrowing).filter(EquipmentBorrowing.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    
    if borrowing.status == 'Returned':
        raise HTTPException(status_code=400, detail="Equipment already returned")

    # Update borrowing record
    borrowing.status = 'Returned'
    borrowing.actual_return_date = datetime.utcnow()
    
    # Update equipment status
    equipment = db.query(Equipment).filter(Equipment.id == borrowing.equipment_id).first()
    if equipment:
        equipment.status = 'Available'
    
    db.commit()
    return {"message": "Equipment returned successfully"}

@router.get("/borrowings", response_model=List[BorrowingResponse])
def get_borrowings(db: Session = Depends(get_db)):
    return db.query(EquipmentBorrowing).all()
