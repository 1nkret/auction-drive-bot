from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime, UTC

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
