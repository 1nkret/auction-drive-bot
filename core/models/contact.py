from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from core.models.base import Base

class ContactRequest(Base):
    __tablename__ = "contact_requests"
    __table_args__ = (PrimaryKeyConstraint("user_id", "car_id"),)

    user_id = Column(Integer, ForeignKey("users.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))
    phone_number = Column(String)
    is_processed = Column(Boolean)
    manager_id = Column(Integer)  # ID of the manager who processed the request
    # relationships
    user = relationship("User", back_populates="contact_requests")
    car = relationship("Car", back_populates="contact_requests")
