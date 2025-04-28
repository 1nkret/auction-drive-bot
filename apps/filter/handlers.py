from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import SearchSettings
from core.middleware.database import DatabaseMiddleware
from apps.filter.cb_data import FilterCBD
from core.enums import SearchSettingsAction, EditSearchSettingsAction
from utils import get_user, build_inline_kb, t

router = Router()
router.callback_query.middleware(DatabaseMiddleware())
router.message.middleware(DatabaseMiddleware())


@router.callback_query(FilterCBD.filter(F.action == SearchSettingsAction.create))
async def setup_filters(callback: CallbackQuery, session: AsyncSession, locale: str, state: FSMContext):
    user = await get_user(session, callback.from_user.id)
    search_settings = SearchSettings(user_id=user.id)
    session.add(search_settings)
    await session.commit()
    await session.refresh(search_settings)
    
    await state.update_data(settings=search_settings)
    
    kb = build_inline_kb(
        sizes=[2, 2, 2, 2, 2, 1, 1],
        buttons={
            t("kb_btn_mark", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.mark, filter_id=search_settings.id).pack(),
            t("kb_btn_model", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.model, filter_id=search_settings.id).pack(),
            t("kb_btn_min_year", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.min_year, filter_id=search_settings.id).pack(),
            t("kb_btn_max_year", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.max_year, filter_id=search_settings.id).pack(),
            t("kb_btn_min_mileage", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.min_mileage, filter_id=search_settings.id).pack(),
            t("kb_btn_max_mileage", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.max_mileage, filter_id=search_settings.id).pack(),
            t("kb_btn_engine", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.engine_type, filter_id=search_settings.id).pack(),
            t("kb_btn_drive", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.drive_type, filter_id=search_settings.id).pack(),
            t("kb_btn_min_price", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.min_price, filter_id=search_settings.id).pack(),
            t("kb_btn_max_price", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.max_price, filter_id=search_settings.id).pack(),
            t("kb_btn_damage", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.allow_damaged, filter_id=search_settings.id).pack(),
            t("kb_btn_done", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.done, filter_id=search_settings.id).pack(),
        }
    )
    
    await callback.message.edit_text(
        t("select_param", locale),
        reply_markup=kb
    )


@router.callback_query(FilterCBD.filter())
async def cb_data_echo(cb: CallbackQuery):
    await cb.answer(f"Selected action: {cb.data}")

# Mark filter handler
# @router.callback_query(F.data == "filter_mark")
# async def set_mark(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(FilterStates.waiting_for_mark)
#     await callback.message.edit_text(
#         "Введите марку автомобиля (например, Toyota, BMW, Mercedes):"
#     )

# @router.message(StateFilter(FilterStates.waiting_for_mark))
# async def process_mark(message: Message, state: FSMContext, session: AsyncSession):
#     user = await session.get(User, message.from_user.id)
#     settings = await session.get(SearchSettings, user.id)
#     settings.mark = message.text
#     await session.commit()
    
#     await state.clear()
#     await message.answer(f"Марка установлена: {message.text}")
#     await setup_filters(message, state)

# # Model filter handler
# @router.callback_query(F.data == "filter_model")
# async def set_model(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(FilterStates.waiting_for_model)
#     await callback.message.edit_text(
#         "Введите модель автомобиля:"
#     )

# @router.message(StateFilter(FilterStates.waiting_for_model))
# async def process_model(message: Message, state: FSMContext, session: AsyncSession):
#     user = await session.get(User, message.from_user.id)
#     settings = await session.get(SearchSettings, user.id)
#     settings.model = message.text
#     await session.commit()
    
#     await state.clear()
#     await message.answer(f"Модель установлена: {message.text}")
#     await setup_filters(message, state)

# # Year filter handler
# @router.callback_query(F.data == "filter_year")
# async def set_year(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(FilterStates.waiting_for_year)
#     await callback.message.edit_text(
#         "Введите диапазон годов (например, 2010-2020):"
#     )

# @router.message(StateFilter(FilterStates.waiting_for_year))
# async def process_year(message: Message, state: FSMContext, session: AsyncSession):
#     try:
#         min_year, max_year = map(int, message.text.split("-"))
#         user = await session.get(User, message.from_user.id)
#         settings = await session.get(SearchSettings, user.id)
#         settings.min_year = min_year
#         settings.max_year = max_year
#         await session.commit()
        
#         await state.clear()
#         await message.answer(f"Диапазон годов установлен: {min_year}-{max_year}")
#         await setup_filters(message, state)
#     except ValueError:
#         await message.answer("Пожалуйста, введите корректный диапазон годов (например, 2010-2020)")

# # Mileage filter handler
# @router.callback_query(F.data == "filter_mileage")
# async def set_mileage(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(FilterStates.waiting_for_mileage)
#     await callback.message.edit_text(
#         "Введите максимальный пробег в километрах:"
#     )

# @router.message(StateFilter(FilterStates.waiting_for_mileage))
# async def process_mileage(message: Message, state: FSMContext, session: AsyncSession):
#     try:
#         mileage = int(message.text)
#         user = await session.get(User, message.from_user.id)
#         settings = await session.get(SearchSettings, user.id)
#         settings.max_mileage = mileage
#         await session.commit()
        
#         await state.clear()
#         await message.answer(f"Максимальный пробег установлен: {mileage} км")
#         await setup_filters(message, state)
#     except ValueError:
#         await message.answer("Пожалуйста, введите корректное число")

# # Engine type filter handler
# @router.callback_query(F.data == "filter_engine")
# async def set_engine_type(callback: CallbackQuery, state: FSMContext):
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Бензин", callback_data="engine_petrol")
#     builder.button(text="Дизель", callback_data="engine_diesel")
#     builder.button(text="Электро", callback_data="engine_electric")
#     builder.button(text="Гибрид", callback_data="engine_hybrid")
#     builder.adjust(2)
    
#     await callback.message.edit_text(
#         "Выберите тип двигателя:",
#         reply_markup=builder.as_markup()
#     )

# @router.callback_query(F.data.startswith("engine_"))
# async def process_engine_type(callback: CallbackQuery, session: AsyncSession):
#     engine_type = callback.data.split("_")[1]
#     user = await session.get(User, callback.from_user.id)
#     settings = await session.get(SearchSettings, user.id)
#     settings.engine_type = engine_type
#     await session.commit()
    
#     await callback.message.edit_text(f"Тип двигателя установлен: {engine_type}")
#     await setup_filters(callback, None)

# # Drive type filter handler
# @router.callback_query(F.data == "filter_drive")
# async def set_drive_type(callback: CallbackQuery, state: FSMContext):
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Передний", callback_data="drive_front")
#     builder.button(text="Задний", callback_data="drive_back")
#     builder.button(text="Полный", callback_data="drive_full")
#     builder.adjust(2)
    
#     await callback.message.edit_text(
#         "Выберите тип привода:",
#         reply_markup=builder.as_markup()
#     )

# @router.callback_query(F.data.startswith("drive_"))
# async def process_drive_type(callback: CallbackQuery, session: AsyncSession):
#     drive_type = callback.data.split("_")[1]
#     user = await session.get(User, callback.from_user.id)
#     settings = await session.get(SearchSettings, user.id)
#     settings.drive_type = drive_type
#     await session.commit()
    
#     await callback.message.edit_text(f"Тип привода установлен: {drive_type}")
#     await setup_filters(callback, None)

# # Price filter handler
# @router.callback_query(F.data == "filter_price")
# async def set_price(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(FilterStates.waiting_for_price)
#     await callback.message.edit_text(
#         "Введите диапазон цен в долларах (например, 10000-20000):"
#     )

# @router.message(StateFilter(FilterStates.waiting_for_price))
# async def process_price(message: Message, state: FSMContext, session: AsyncSession):
#     try:
#         min_price, max_price = map(int, message.text.split("-"))
#         user = await session.get(User, message.from_user.id)
#         settings = await session.get(SearchSettings, user.id)
#         settings.min_price = min_price
#         settings.max_price = max_price
#         await session.commit()
        
#         await state.clear()
#         await message.answer(f"Диапазон цен установлен: ${min_price}-${max_price}")
#         await setup_filters(message, state)
#     except ValueError:
#         await message.answer("Пожалуйста, введите корректный диапазон цен (например, 10000-20000)")

# # Damage filter handler
# @router.callback_query(F.data == "filter_damage")
# async def set_damage(callback: CallbackQuery, state: FSMContext):
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Да", callback_data="damage_yes")
#     builder.button(text="Нет", callback_data="damage_no")
#     builder.button(text="Не важно", callback_data="damage_any")
#     builder.adjust(2)
    
#     await callback.message.edit_text(
#         "Показывать автомобили с повреждениями?",
#         reply_markup=builder.as_markup()
#     )

# @router.callback_query(F.data.startswith("damage_"))
# async def process_damage(callback: CallbackQuery, session: AsyncSession):
#     damage_setting = callback.data.split("_")[1]
#     user = await session.get(User, callback.from_user.id)
#     settings = await session.get(SearchSettings, user.id)
#     settings.allow_damaged = damage_setting != "no"
#     await session.commit()
    
#     await callback.message.edit_text(
#         f"Настройка повреждений установлена: {'Да' if damage_setting == 'yes' else 'Нет' if damage_setting == 'no' else 'Не важно'}"
#     )
#     await setup_filters(callback, None)

# # Finish filter setup
# @router.callback_query(F.data == "filters_done")
# async def finish_filters(callback: CallbackQuery, session: AsyncSession):
#     user = await session.get(User, callback.from_user.id)
#     settings = await session.get(SearchSettings, user.id)
    
#     # Show current settings
#     settings_text = (
#         f"Текущие настройки фильтров:\n\n"
#         f"Марка: {settings.mark or 'Не указана'}\n"
#         f"Модель: {settings.model or 'Не указана'}\n"
#         f"Год: {f'{settings.min_year}-{settings.max_year}' if settings.min_year and settings.max_year else 'Не указан'}\n"
#         f"Пробег: {f'до {settings.max_mileage} км' if settings.max_mileage else 'Не указан'}\n"
#         f"Тип двигателя: {settings.engine_type or 'Не указан'}\n"
#         f"Привод: {settings.drive_type or 'Не указан'}\n"
#         f"Цена: {f'${settings.min_price}-${settings.max_price}' if settings.min_price and settings.max_price else 'Не указана'}\n"
#         f"Повреждения: {'Разрешены' if settings.allow_damaged else 'Запрещены'}"
#     )
    
#     builder = InlineKeyboardBuilder()
#     builder.button(text="🔍 Начать поиск", callback_data="search_cars")
#     builder.button(text="⚙️ Изменить фильтры", callback_data="setup_filters")
    
#     await callback.message.edit_text(settings_text, reply_markup=builder.as_markup()) 