from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.models.base import BaseModel

class SearchSettings(BaseModel):
    __tablename__ = "search_settings"

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    mark = Column(String, nullable=True)
    model = Column(String, nullable=True)
    min_year = Column(Integer, nullable=True)
    max_year = Column(Integer, nullable=True)
    min_mileage = Column(Integer, nullable=True)
    max_mileage = Column(Integer, nullable=True)
    engine_type = Column(String, nullable=True)  # petrol/electro/hybrid/diesel
    drive_type = Column(String, nullable=True)  # front/back/full
    min_price = Column(Integer, nullable=True)
    max_price = Column(Integer, nullable=True)
    allow_damaged = Column(Boolean, default=True)

    user = relationship("User", backref="search_settings") 