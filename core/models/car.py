from sqlalchemy import Column, String, Integer, Boolean, JSON
from sqlalchemy.orm import relationship
from core.models.base import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mark = Column(String)
    model = Column(String)
    year = Column(Integer)
    mileage = Column(Integer)
    engine_type = Column(String)  # petrol/electro/hybrid/diesel
    engine_volume = Column(String)  # e.g., "2.0"
    drive_type = Column(String)  # front/back/full
    price = Column(Integer)  # in dollars
    has_damage = Column(Boolean)
    photos = Column(JSON)  # list of photo URLs
    is_active = Column(Boolean)
    manager_id = Column(Integer)  # ID of the manager handling this car 
    # relationships
    contact_requests = relationship("ContactRequest", back_populates="car", cascade="all, delete-orphan")
