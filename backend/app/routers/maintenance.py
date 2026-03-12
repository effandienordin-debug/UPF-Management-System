from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..auth import get_current_user, check_role
from ..models.maintenance import MaintenanceRequest, TechnicianAssignment
from ..models.user import User
from ..schemas.maintenance import MaintenanceRequestResponse, MaintenanceRequestCreate, TechnicianAssignmentResponse

router = APIRouter()

@router.get("/", response_model=List[MaintenanceRequestResponse])
def get_maintenance_requests(db: Session = Depends(get_db)):
    return db.query(MaintenanceRequest).all()

@router.post("/", response_model=MaintenanceRequestResponse)
def create_maintenance_request(request_in: MaintenanceRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_request = MaintenanceRequest(
        **request_in.dict(),
        user_id=current_user.id,
        status='Open'
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.post("/assign-technician", response_model=TechnicianAssignmentResponse, dependencies=[Depends(check_role(["UPF Admin"]))])
def assign_technician(assignment_in: dict, db: Session = Depends(get_db)):
    new_assignment = TechnicianAssignment(
        maintenance_id=assignment_in["maintenance_id"],
        technician_id=assignment_in["technician_id"],
        status='Assigned'
    )
    # Update request status to 'Assigned'
    request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == assignment_in["maintenance_id"]).first()
    if request:
        request.status = 'Assigned'
        
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.patch("/{request_id}/status")
def update_maintenance_status(request_id: UUID, status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    
    # Check if user is technician or admin
    if current_user.role not in ["Technician", "UPF Admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    request.status = status
    db.commit()
    return {"message": f"Maintenance request status updated to {status}"}
