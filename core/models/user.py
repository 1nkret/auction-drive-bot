from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from core.models.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_notification = Column(DateTime, nullable=True)
    notification_frequency = Column(Integer, default=1)  # days between notifications
    notification_count = Column(Integer, default=0)  # count of received notifications
    # relationships
    search_settings = relationship("SearchSettings", back_populates="user", cascade="all, delete-orphan") 
    contact_requests = relationship("ContactRequest", back_populates="user", cascade="all, delete-orphan")

