from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from core.enums import EngineTypeEnum, DriveTypeEnum

class SearchSettingsBase(BaseModel):
    mark: Optional[str] = None
    model: Optional[str] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    min_mileage: Optional[int] = None
    max_mileage: Optional[int] = None
    engine_type: Optional[str] = None
    drive_type: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    allow_damaged: bool = False

class SearchSettingsCreate(SearchSettingsBase):
    user_id: int

class SearchSettingsUpdate(SearchSettingsBase):
    id: int

class SearchSettingsInDB(SearchSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 


class SearchSettingsSchema(SearchSettingsBase):
    id: Optional[int] = None

    model_config=ConfigDict(from_attributes=True)
