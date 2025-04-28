from enum import Enum


class EngineType(Enum):
    petrol = "petrol"
    electro = "electro"
    hybrid = "hybrid"
    diesel = "diesel"


class DriveType(Enum):
    front = "front"
    back = "back"
    full = "full"