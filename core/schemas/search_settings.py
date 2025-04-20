from pydantic import BaseModel, Field
from typing import Optional
from ..enums.engine_type import EngineType
from ..enums.drive_type import DriveType

class SearchSettingsBase(BaseModel):
    mark: Optional[str] = None
    model: Optional[str] = None
    min_year: Optional[int] = Field(None, ge=1900)
    max_year: Optional[int] = Field(None, le=2100)
    min_mileage: Optional[int] = Field(None, ge=0)
    max_mileage: Optional[int] = Field(None, ge=0)
    engine_type: Optional[EngineType] = None
    drive_type: Optional[DriveType] = None
    min_price: Optional[int] = Field(None, ge=0)
    max_price: Optional[int] = Field(None, ge=0)
    allow_damaged: bool = True

class SearchSettingsCreate(SearchSettingsBase):
    user_id: int

class SearchSettingsUpdate(SearchSettingsBase):
    pass

class SearchSettingsInDB(SearchSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 