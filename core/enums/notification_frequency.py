from enum import Enum

class NotificationFrequency(int, Enum):
    DAILY = 1
    EVERY_OTHER_DAY = 2
    WEEKLY = 7

    @classmethod
    def get_display_name(cls, value: int) -> str:
        display_names = {
            cls.DAILY: "Ежедневно",
            cls.EVERY_OTHER_DAY: "Через день",
            cls.WEEKLY: "Еженедельно"
        }
        return display_names.get(value, str(value)) 