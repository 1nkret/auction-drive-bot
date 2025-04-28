from utils.build_inline_kb import build_inline_kb
from apps.filter.cb_data import FilterCBD
from core.enums import SearchSettingsAction


def get_main_menu_kb():
    sizes = [1, 2]
    buttons = {
        "Фільтри": FilterCBD(action=SearchSettingsAction.create).pack(),
        "Про проект": "about",
        "Довідка": "help",
    }
    return build_inline_kb(
        sizes=sizes,
        buttons=buttons,
    )
