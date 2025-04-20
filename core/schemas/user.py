from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from ..enums.notification_frequency import NotificationFrequency

class UserBase(BaseModel):
    telegram_id: int
    phone_number: Optional[str] = None
    is_active: bool = True
    last_notification: Optional[datetime] = None
    notification_frequency: NotificationFrequency = NotificationFrequency.DAILY
    notification_count: int = 0

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None
    notification_frequency: Optional[NotificationFrequency] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 