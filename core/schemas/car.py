from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from ..enums.engine_type import EngineType
from ..enums.drive_type import DriveType

class CarBase(BaseModel):
    mark: str
    model: str
    year: int = Field(..., ge=1900, le=datetime.now().year)
    mileage: int = Field(..., ge=0)
    engine_type: EngineType
    engine_volume: Optional[str] = None
    drive_type: DriveType
    price: int = Field(..., ge=0)
    has_damage: bool = False
    photos: List[str]
    is_active: bool = True
    manager_id: Optional[int] = None

class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    mark: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    mileage: Optional[int] = Field(None, ge=0)
    engine_type: Optional[EngineType] = None
    engine_volume: Optional[str] = None
    drive_type: Optional[DriveType] = None
    price: Optional[int] = Field(None, ge=0)
    has_damage: Optional[bool] = None
    photos: Optional[List[str]] = None
    is_active: Optional[bool] = None
    manager_id: Optional[int] = None

class CarInDB(CarBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 