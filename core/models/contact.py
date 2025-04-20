from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.models.base import BaseModel

class ContactRequest(BaseModel):
    __tablename__ = "contact_requests"

    user_id = Column(Integer, ForeignKey("users.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))
    phone_number = Column(String, nullable=True)
    is_processed = Column(Boolean, default=False)
    manager_id = Column(Integer, nullable=True)  # ID of the manager who processed the request

    user = relationship("User", backref="contact_requests")
    car = relationship("Car", backref="contact_requests") 