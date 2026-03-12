from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..auth import get_current_user, check_role
from ..models.stationery import StationeryItem, StationeryTransaction, StationeryTransactionItem
from ..models.user import User
from ..schemas.stationery import StationeryItemResponse, StationeryItemCreate, StationeryTransactionCreate, StationeryTransactionResponse

router = APIRouter()

@router.get("/items", response_model=List[StationeryItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(StationeryItem).all()

@router.post("/items", response_model=StationeryItemResponse, dependencies=[Depends(check_role(["UPF Admin"]))])
def create_item(item_in: StationeryItemCreate, db: Session = Depends(get_db)):
    new_item = StationeryItem(**item_in.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.put("/items/{item_id}", response_model=StationeryItemResponse, dependencies=[Depends(check_role(["UPF Admin"]))])
def update_item(item_id: UUID, item_in: StationeryItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(StationeryItem).filter(StationeryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item_in.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}", dependencies=[Depends(check_role(["UPF Admin"]))])
def delete_item(item_id: UUID, db: Session = Depends(get_db)):
    db_item = db.query(StationeryItem).filter(StationeryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}

@router.post("/transactions", response_model=StationeryTransactionResponse)
def create_transaction(transaction_in: StationeryTransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validate stock and create transaction
    new_transaction = StationeryTransaction(
        staff_id=transaction_in.staff_id,
        issued_by=current_user.id,
        department=transaction_in.department,
        total_items=len(transaction_in.items)
    )
    db.add(new_transaction)
    db.flush() # Get transaction ID

    for item_data in transaction_in.items:
        db_item = db.query(StationeryItem).filter(StationeryItem.id == item_data.item_id).first()
        if not db_item:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Item {item_data.item_id} not found")
        
        if db_item.stock_quantity < item_data.quantity:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {db_item.item_name}")
        
        # Deduct stock
        db_item.stock_quantity -= item_data.quantity
        
        # Add transaction item
        new_tx_item = StationeryTransactionItem(
            transaction_id=new_transaction.id,
            item_id=item_data.item_id,
            quantity=item_data.quantity
        )
        db.add(new_tx_item)

    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.get("/transactions", response_model=List[StationeryTransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(StationeryTransaction).all()
