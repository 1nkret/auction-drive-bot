from typing import Optional
from aiogram.filters.callback_data import CallbackData
from pydantic import model_validator
from core.enums import SearchSettingsAction, EditSearchSettingsAction


class FilterCBD(CallbackData, prefix="filter"):
    action: SearchSettingsAction
    edit_action: Optional[EditSearchSettingsAction] = None
    filter_id: Optional[int] = None
    
    @model_validator(mode="before")
    def validate_logic(cls, values):
        action = values.get('action')
        edit_action = values.get('edit_action')
        filter_id = values.get('filter_id')

        if action == SearchSettingsAction.edit:
            if not edit_action or filter_id is None:
                raise ValueError("For 'edit' action, both 'edit_action' and 'filter_id' must be provided.")
        elif action == SearchSettingsAction.delete:
            if filter_id is None:
                raise ValueError(f"For 'delete' action, 'filter_id' must be provided.")
        
        return values
