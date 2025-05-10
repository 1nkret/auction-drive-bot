from utils.build_inline_kb import build_inline_kb
from apps.filter.cb_data import FilterCBD
from core.enums import SearchSettingsAction
from utils.locales import t


def get_main_menu_kb(locale: str = "en"):
    sizes = [1, 2]
    buttons = {
        t("kb_filters", locale): FilterCBD(action=SearchSettingsAction.read).pack(),
        t("kb_about", locale): "about",
        t("kb_dovidka", locale): "help",
    }
    return build_inline_kb(
        sizes=sizes,
        buttons=buttons,
    )
