from enum import Enum

class DriveType(str, Enum):
    FRONT = "front"
    BACK = "back"
    FULL = "full"

    @classmethod
    def get_display_name(cls, value: str) -> str:
        display_names = {
            cls.FRONT: "Передний",
            cls.BACK: "Задний",
            cls.FULL: "Полный"
        }
        return display_names.get(value, value) 