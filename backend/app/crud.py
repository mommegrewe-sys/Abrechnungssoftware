from sqlalchemy.orm import Session
from app from app from app import models, schemas

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
    return db_partner