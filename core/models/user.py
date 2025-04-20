from sqlalchemy import Column, String, Integer, Boolean, DateTime
from core.models.base import BaseModel
from datetime import datetime

class User(BaseModel):
    __tablename__ = "users"

    telegram_id = Column(Integer, unique=True, index=True)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_notification = Column(DateTime, nullable=True)
    notification_frequency = Column(Integer, default=1)  # days between notifications
    notification_count = Column(Integer, default=0)  # count of received notifications
    search_settings = Column(String, nullable=True)  # JSON string of search preferences 