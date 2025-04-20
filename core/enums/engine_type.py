from enum import Enum

class EngineType(str, Enum):
    PETROL = "petrol"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"

    @classmethod
    def get_display_name(cls, value: str) -> str:
        display_names = {
            cls.PETROL: "Бензин",
            cls.DIESEL: "Дизель",
            cls.ELECTRIC: "Электро",
            cls.HYBRID: "Гибрид"
        }
        return display_names.get(value, value) 