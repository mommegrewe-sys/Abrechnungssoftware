import os
from pathlib import Path

# --- Ordnerstruktur ---
folders = [
    "app/routers"
]

files_content = {
    "app/main.py": '''from fastapi import FastAPI
from app.routers import partners
from app.database import Base, engine

app = FastAPI(title="Abrechnungssoftware API")

Base.metadata.create_all(bind=engine)

app.include_router(partners.router, prefix="/partners", tags=["Partners"])''',

    "app/database.py": '''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Adjust these to your local PostgreSQL setup
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Abrechnung"

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()''',

    "app/models.py": '''from sqlalchemy import Column, Integer, String, Boolean, Date
from app.database import Base

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email_contact = Column(String(255))
    city = Column(String(100))
    postal_code = Column(String(20))
    street = Column(String(100))
    house_number = Column(String(20))
    active = Column(Boolean, default=True)
    created_at = Column(Date)''',

    "app/schemas.py": '''from pydantic import BaseModel
from typing import Optional
from datetime import date

class PartnerBase(BaseModel):
    name: str
    email_contact: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    active: Optional[bool] = True

class PartnerCreate(PartnerBase):
    pass

class Partner(PartnerBase):
    id: int
    created_at: Optional[date] = None

    class Config:
        orm_mode = True''',

    "app/crud.py": '''from sqlalchemy.orm import Session
from app import models, schemas

def get_partners(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Partner).offset(skip).limit(limit).all()

def get_partner(db: Session, partner_id: int):
    return db.query(models.Partner).filter(models.Partner.id == partner_id).first()

def create_partner(db: Session, partner: schemas.PartnerCreate):
    db_partner = models.Partner(**partner.dict())
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner

def update_partner(db: Session, partner_id: int, partner: schemas.PartnerCreate):
    db_partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if not db_partner:
        return None
    for key, value in partner.dict().items():
        setattr(db_partner, key, value)
    db.commit()
    db.refresh(db_partner)
    return db_partner

def delete_partner(db: Session, partner_id: int):
    db_partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if db_partner:
        db.delete(db_partner)
        db.commit()
    return db_partner''',

    "app/routers/partners.py": '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
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
    return {"ok": True}''',

    "requirements.txt": '''fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
python-dotenv'''
}

# --- Erstellung ---
base_dir = Path(__file__).parent

for folder in folders:
    os.makedirs(base_dir / folder, exist_ok=True)

for path, content in files_content.items():
    file_path = base_dir / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)

print("✅ Backend setup complete! You can now run:")
print("cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload")
