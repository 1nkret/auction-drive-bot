from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ContactRequestBase(BaseModel):
    user_id: int
    car_id: int
    phone_number: Optional[str] = None
    is_processed: bool = False
    manager_id: Optional[int] = None

class ContactRequestCreate(ContactRequestBase):
    pass

class ContactRequestUpdate(BaseModel):
    phone_number: Optional[str] = None
    is_processed: Optional[bool] = None
    manager_id: Optional[int] = None

class ContactRequestInDB(ContactRequestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 