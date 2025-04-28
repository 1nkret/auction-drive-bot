from enum import Enum


class SearchSettingsAction(Enum):
    read = "read"
    create = "create"
    edit = "edit"
    delete = "delete"

class EditSearchSettingsAction(Enum):
    mark = "mark"
    model = "model"
    min_year = "min_year"
    max_year = "max_year"
    min_mileage = "min_mileage"
    max_mileage = "max_mileage"
    engine_type = "engine_type"
    drive_type = "drive_type"
    min_price = "min_price"
    max_price = "max_price"
    allow_damaged = "allow_damaged"
    done = "done"
