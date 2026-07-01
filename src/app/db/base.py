from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func
from datetime import datetime

class Base(DeclarativeBase):
    """所有ORM表模型的父类"""
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    