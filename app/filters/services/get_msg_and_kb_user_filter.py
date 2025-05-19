from app.filters.cb_data import FilterCBD
from core.enums import SearchSettingsAction
from core.models import SearchSettings
from core.settings import settings
from utils import build_inline_kb, t


from aiogram.types import InlineKeyboardMarkup


from typing import Tuple


def get_msg_and_kb_user_filter(user_filters: list[SearchSettings], show_filter: SearchSettings, locale: str) -> Tuple[str, InlineKeyboardMarkup]:
    text = t("represent_filter", locale)
    text = text.format(
        mark=show_filter.mark or "...",
        model=show_filter.model or "...",
        min_year=show_filter.min_year or "...",
        max_year=show_filter.max_year or "...",
        min_mileage=show_filter.min_mileage or "...",
        max_mileage=show_filter.max_mileage or "...",
        engine_type=show_filter.engine_type or "...",
        drive_type=show_filter.drive_type or "...",
        min_price=show_filter.min_price or "...",
        max_price=show_filter.max_price or "...",
        allow_damaged="✅" if show_filter.allow_damaged else "🚫"
    )
    buttons = dict()
    sizes = []
    cur_ind = user_filters.index(show_filter)
    filters_count = len(user_filters)
    buttons[t("edit", locale)] = FilterCBD(action=SearchSettingsAction.edit, filter_id=show_filter.id).pack()
    sizes.append(1)
    buttons[t("delete", locale)] = FilterCBD(action=SearchSettingsAction.delete, filter_id=show_filter.id).pack()
    sizes.append(1)
    has_prev: bool = False
    if cur_ind != 0:
        buttons[t("prev", locale)] = FilterCBD(action=SearchSettingsAction.read, filter_id=user_filters[cur_ind-1].id).pack()
        has_prev = True
        sizes.append(1)
    if cur_ind < filters_count-1:
        buttons[t("next", locale)] = FilterCBD(action=SearchSettingsAction.read, filter_id=user_filters[cur_ind+1].id).pack()
        if has_prev:
            sizes.pop()
            sizes.append(2)
        else:
            sizes.append(1)
    if filters_count < settings.max_filters:
        buttons[t("new_filter", locale)] = FilterCBD(action=SearchSettingsAction.create).pack()
        sizes.append(1)
    return text, build_inline_kb(sizes=sizes, buttons=buttons)