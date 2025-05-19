from app.filters.services.get_msg_and_kb_edit_msg import get_msg_and_kb_edit_msg
from core.models import SearchSettings
from core.schemas.search_settings import SearchSettingsSchema


from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


async def setup_filter_settings_for_editing(
    callback: CallbackQuery,
    state: FSMContext,
    locale: str,
    filt_obj: SearchSettings = None
    ):
    settings_schema = SearchSettingsSchema(
        id=filt_obj.id if filt_obj else None,
        mark=filt_obj.mark if filt_obj else None,
        model=filt_obj.model if filt_obj else None,
        min_year=filt_obj.min_year if filt_obj else None,
        max_year=filt_obj.max_year if filt_obj else None,
        min_mileage=filt_obj.min_mileage if filt_obj else None,
        max_mileage=filt_obj.max_mileage if filt_obj else None,
        engine_type=filt_obj.engine_type if filt_obj else None,
        drive_type=filt_obj.drive_type if filt_obj else None,
        min_price=filt_obj.min_price if filt_obj else None,
        max_price=filt_obj.max_price if filt_obj else None,
        allow_damaged=filt_obj.allow_damaged if filt_obj else None
    ) if filt_obj else SearchSettingsSchema()

    await state.set_data({
        "settings": settings_schema.model_dump(),
        "edit_settings_msg": callback.message
    })

    msg_text, kb = get_msg_and_kb_edit_msg(locale, settings_schema)

    await callback.message.edit_text(text=msg_text, reply_markup=kb)