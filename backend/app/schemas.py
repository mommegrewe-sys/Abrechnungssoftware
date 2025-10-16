from pydantic import BaseModel
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
    from_attributes = True
