from sqlalchemy import Column, String, Integer, Boolean, JSON
from core.models.base import BaseModel

class Car(BaseModel):
    __tablename__ = "cars"

    mark = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)
    mileage = Column(Integer)
    engine_type = Column(String)  # petrol/electro/hybrid/diesel
    engine_volume = Column(String, nullable=True)  # e.g., "2.0", "V6"
    drive_type = Column(String)  # front/back/full
    price = Column(Integer)  # in dollars
    has_damage = Column(Boolean, default=False)
    photos = Column(JSON)  # list of photo URLs
    is_active = Column(Boolean, default=True)
    manager_id = Column(Integer, nullable=True)  # ID of the manager handling this car 