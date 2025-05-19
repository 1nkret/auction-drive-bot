from app.filters.services.get_msg_and_kb_edit_msg import get_msg_and_kb_edit_msg


from aiogram.types import Message


async def update_state_data_and_editing_message(msg, state, locale, data, settings):
    await state.update_data(settings=settings.model_dump())
    msg_to_edit: Message = data.get("edit_settings_msg")
    text, kb = get_msg_and_kb_edit_msg(locale, settings)
    await msg.delete()
    await msg_to_edit.edit_text(text=text, reply_markup=kb)