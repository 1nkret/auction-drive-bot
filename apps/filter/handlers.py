from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User, SearchSettings
from typing import Optional

router = Router()

class FilterStates(StatesGroup):
    waiting_for_mark = State()
    waiting_for_model = State()
    waiting_for_year = State()
    waiting_for_mileage = State()
    waiting_for_engine_type = State()
    waiting_for_drive_type = State()
    waiting_for_price = State()
    waiting_for_damage = State()

# Start command handler
@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession):
    # Create or get user
    user = await session.get(User, message.from_user.id)
    if not user:
        user = User(telegram_id=message.from_user.id)
        session.add(user)
        await session.commit()
    
    # Create or get search settings
    settings = await session.get(SearchSettings, user.id)
    if not settings:
        settings = SearchSettings(user_id=user.id)
        session.add(settings)
        await session.commit()
    
    # Send welcome message with filter setup
    builder = InlineKeyboardBuilder()
    builder.button(text="⚙️ Настроить фильтры", callback_data="setup_filters")
    builder.button(text="🔍 Поиск по текущим фильтрам", callback_data="search_cars")
    
    await message.answer(
        "👋 Добро пожаловать в бот поиска автомобилей!\n\n"
        "Здесь вы можете настроить фильтры для поиска автомобилей и получать уведомления о новых предложениях.",
        reply_markup=builder.as_markup()
    )

# Filter setup handlers
@router.callback_query(F.data == "setup_filters")
async def setup_filters(callback: CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="Марка", callback_data="filter_mark")
    builder.button(text="Модель", callback_data="filter_model")
    builder.button(text="Год", callback_data="filter_year")
    builder.button(text="Пробег", callback_data="filter_mileage")
    builder.button(text="Тип двигателя", callback_data="filter_engine")
    builder.button(text="Привод", callback_data="filter_drive")
    builder.button(text="Цена", callback_data="filter_price")
    builder.button(text="Повреждения", callback_data="filter_damage")
    builder.button(text="✅ Готово", callback_data="filters_done")
    builder.adjust(2)
    
    await callback.message.edit_text(
        "Выберите параметр для настройки:",
        reply_markup=builder.as_markup()
    )

# Mark filter handler
@router.callback_query(F.data == "filter_mark")
async def set_mark(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.waiting_for_mark)
    await callback.message.edit_text(
        "Введите марку автомобиля (например, Toyota, BMW, Mercedes):"
    )

@router.message(StateFilter(FilterStates.waiting_for_mark))
async def process_mark(message: Message, state: FSMContext, session: AsyncSession):
    user = await session.get(User, message.from_user.id)
    settings = await session.get(SearchSettings, user.id)
    settings.mark = message.text
    await session.commit()
    
    await state.clear()
    await message.answer(f"Марка установлена: {message.text}")
    await setup_filters(message, state)

# Model filter handler
@router.callback_query(F.data == "filter_model")
async def set_model(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.waiting_for_model)
    await callback.message.edit_text(
        "Введите модель автомобиля:"
    )

@router.message(StateFilter(FilterStates.waiting_for_model))
async def process_model(message: Message, state: FSMContext, session: AsyncSession):
    user = await session.get(User, message.from_user.id)
    settings = await session.get(SearchSettings, user.id)
    settings.model = message.text
    await session.commit()
    
    await state.clear()
    await message.answer(f"Модель установлена: {message.text}")
    await setup_filters(message, state)

# Year filter handler
@router.callback_query(F.data == "filter_year")
async def set_year(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.waiting_for_year)
    await callback.message.edit_text(
        "Введите диапазон годов (например, 2010-2020):"
    )

@router.message(StateFilter(FilterStates.waiting_for_year))
async def process_year(message: Message, state: FSMContext, session: AsyncSession):
    try:
        min_year, max_year = map(int, message.text.split("-"))
        user = await session.get(User, message.from_user.id)
        settings = await session.get(SearchSettings, user.id)
        settings.min_year = min_year
        settings.max_year = max_year
        await session.commit()
        
        await state.clear()
        await message.answer(f"Диапазон годов установлен: {min_year}-{max_year}")
        await setup_filters(message, state)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный диапазон годов (например, 2010-2020)")

# Mileage filter handler
@router.callback_query(F.data == "filter_mileage")
async def set_mileage(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.waiting_for_mileage)
    await callback.message.edit_text(
        "Введите максимальный пробег в километрах:"
    )

@router.message(StateFilter(FilterStates.waiting_for_mileage))
async def process_mileage(message: Message, state: FSMContext, session: AsyncSession):
    try:
        mileage = int(message.text)
        user = await session.get(User, message.from_user.id)
        settings = await session.get(SearchSettings, user.id)
        settings.max_mileage = mileage
        await session.commit()
        
        await state.clear()
        await message.answer(f"Максимальный пробег установлен: {mileage} км")
        await setup_filters(message, state)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число")

# Engine type filter handler
@router.callback_query(F.data == "filter_engine")
async def set_engine_type(callback: CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="Бензин", callback_data="engine_petrol")
    builder.button(text="Дизель", callback_data="engine_diesel")
    builder.button(text="Электро", callback_data="engine_electric")
    builder.button(text="Гибрид", callback_data="engine_hybrid")
    builder.adjust(2)
    
    await callback.message.edit_text(
        "Выберите тип двигателя:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("engine_"))
async def process_engine_type(callback: CallbackQuery, session: AsyncSession):
    engine_type = callback.data.split("_")[1]
    user = await session.get(User, callback.from_user.id)
    settings = await session.get(SearchSettings, user.id)
    settings.engine_type = engine_type
    await session.commit()
    
    await callback.message.edit_text(f"Тип двигателя установлен: {engine_type}")
    await setup_filters(callback, None)

# Drive type filter handler
@router.callback_query(F.data == "filter_drive")
async def set_drive_type(callback: CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="Передний", callback_data="drive_front")
    builder.button(text="Задний", callback_data="drive_back")
    builder.button(text="Полный", callback_data="drive_full")
    builder.adjust(2)
    
    await callback.message.edit_text(
        "Выберите тип привода:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("drive_"))
async def process_drive_type(callback: CallbackQuery, session: AsyncSession):
    drive_type = callback.data.split("_")[1]
    user = await session.get(User, callback.from_user.id)
    settings = await session.get(SearchSettings, user.id)
    settings.drive_type = drive_type
    await session.commit()
    
    await callback.message.edit_text(f"Тип привода установлен: {drive_type}")
    await setup_filters(callback, None)

# Price filter handler
@router.callback_query(F.data == "filter_price")
async def set_price(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.waiting_for_price)
    await callback.message.edit_text(
        "Введите диапазон цен в долларах (например, 10000-20000):"
    )

@router.message(StateFilter(FilterStates.waiting_for_price))
async def process_price(message: Message, state: FSMContext, session: AsyncSession):
    try:
        min_price, max_price = map(int, message.text.split("-"))
        user = await session.get(User, message.from_user.id)
        settings = await session.get(SearchSettings, user.id)
        settings.min_price = min_price
        settings.max_price = max_price
        await session.commit()
        
        await state.clear()
        await message.answer(f"Диапазон цен установлен: ${min_price}-${max_price}")
        await setup_filters(message, state)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный диапазон цен (например, 10000-20000)")

# Damage filter handler
@router.callback_query(F.data == "filter_damage")
async def set_damage(callback: CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="damage_yes")
    builder.button(text="Нет", callback_data="damage_no")
    builder.button(text="Не важно", callback_data="damage_any")
    builder.adjust(2)
    
    await callback.message.edit_text(
        "Показывать автомобили с повреждениями?",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("damage_"))
async def process_damage(callback: CallbackQuery, session: AsyncSession):
    damage_setting = callback.data.split("_")[1]
    user = await session.get(User, callback.from_user.id)
    settings = await session.get(SearchSettings, user.id)
    settings.allow_damaged = damage_setting != "no"
    await session.commit()
    
    await callback.message.edit_text(
        f"Настройка повреждений установлена: {'Да' if damage_setting == 'yes' else 'Нет' if damage_setting == 'no' else 'Не важно'}"
    )
    await setup_filters(callback, None)

# Finish filter setup
@router.callback_query(F.data == "filters_done")
async def finish_filters(callback: CallbackQuery, session: AsyncSession):
    user = await session.get(User, callback.from_user.id)
    settings = await session.get(SearchSettings, user.id)
    
    # Show current settings
    settings_text = (
        f"Текущие настройки фильтров:\n\n"
        f"Марка: {settings.mark or 'Не указана'}\n"
        f"Модель: {settings.model or 'Не указана'}\n"
        f"Год: {f'{settings.min_year}-{settings.max_year}' if settings.min_year and settings.max_year else 'Не указан'}\n"
        f"Пробег: {f'до {settings.max_mileage} км' if settings.max_mileage else 'Не указан'}\n"
        f"Тип двигателя: {settings.engine_type or 'Не указан'}\n"
        f"Привод: {settings.drive_type or 'Не указан'}\n"
        f"Цена: {f'${settings.min_price}-${settings.max_price}' if settings.min_price and settings.max_price else 'Не указана'}\n"
        f"Повреждения: {'Разрешены' if settings.allow_damaged else 'Запрещены'}"
    )
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🔍 Начать поиск", callback_data="search_cars")
    builder.button(text="⚙️ Изменить фильтры", callback_data="setup_filters")
    
    await callback.message.edit_text(settings_text, reply_markup=builder.as_markup()) 