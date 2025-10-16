from sqlalchemy import Column, Integer, String, Boolean, Date
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
    created_at = Column(Date)