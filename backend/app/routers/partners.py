from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app from app from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Partner])
def read_partners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_partners(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Partner)
def create_partner(partner: schemas.PartnerCreate, db: Session = Depends(get_db)):
    return crud.create_partner(db, partner)

@router.put("/{partner_id}", response_model=schemas.Partner)
def update_partner(partner_id: int, partner: schemas.PartnerCreate, db: Session = Depends(get_db)):
    updated = crud.update_partner(db, partner_id, partner)
    if not updated:
        raise HTTPException(status_code=404, detail="Partner not found")
    return updated

@router.delete("/{partner_id}")
def delete_partner(partner_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_partner(db, partner_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"ok": True}