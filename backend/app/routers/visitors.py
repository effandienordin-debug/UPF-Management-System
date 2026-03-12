from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..auth import get_current_user, check_role
from ..models.visitor import Visitor, VisitorPass
from ..models.user import User
from ..schemas.visitor import VisitorResponse, VisitorCreate, VisitorPassResponse
from ..utils.qr_utils import generate_visitor_qr
import uuid

router = APIRouter()

@router.get("/", response_model=List[VisitorResponse])
def get_visitors(db: Session = Depends(get_db)):
    return db.query(Visitor).all()

@router.post("/", response_model=VisitorResponse)
def register_visitor(visitor_in: VisitorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_visitor = Visitor(
        **visitor_in.dict(),
        host_id=current_user.id,
        status='Registered'
    )
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)
    
    # Generate Visitor Pass
    pass_code = str(uuid.uuid4())[:8].upper()
    qr_path = generate_visitor_qr(new_visitor.id, pass_code)
    
    new_pass = VisitorPass(
        visitor_id=new_visitor.id,
        pass_code=pass_code,
        qr_code_path=qr_path
    )
    db.add(new_pass)
    db.commit()
    
    return new_visitor

@router.patch("/{visitor_id}/check-in", dependencies=[Depends(check_role(["Security Officer", "UPF Admin"]))])
def check_in_visitor(visitor_id: UUID, db: Session = Depends(get_db)):
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    
    visitor.status = 'Checked-in'
    db.commit()
    return {"message": "Visitor checked in successfully"}

@router.patch("/{visitor_id}/check-out", dependencies=[Depends(check_role(["Security Officer", "UPF Admin"]))])
def check_out_visitor(visitor_id: UUID, db: Session = Depends(get_db)):
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    
    visitor.status = 'Checked-out'
    db.commit()
    return {"message": "Visitor checked out successfully"}
