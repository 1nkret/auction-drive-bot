from enum import Enum


class EngineTypeEnum(Enum):
    PETROL = "petrol"
    ELECTRO = "electro"
    HYBRID = "hybrid"
    DIESEL = "diesel"


class DriveTypeEnum(Enum):
    FRONT = "front"
    BACK = "back"
    FULL = "full"