from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment="账号")
    password_hash: Mapped[str] = mapped_column(String(255), comment="加密密码")