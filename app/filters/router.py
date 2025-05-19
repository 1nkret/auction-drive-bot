from aiogram import Router

from core.middleware.database import DatabaseMiddleware
from app.filters.handlers import *


router = Router(name="filters")
router.callback_query.middleware(DatabaseMiddleware())
router.message.middleware(DatabaseMiddleware())

router.include_routers(
    delete_filter.router,
    edit_allow_damaged.router,
    edit_drive_type.router,
    edit_engine_type.router,
    edit_mark.router,
    edit_max_mileage.router,
    edit_max_price.router,
    edit_max_year.router,
    edit_min_mileage.router,
    edit_min_price.router,
    edit_min_year.router,
    edit_model.router,
    read_filter.router,
    save_filter.router,
    setup_editing_filter.router,
)

__all__ = [
    "router",
]
