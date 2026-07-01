from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, SmallInteger, Index

class ViewConfig(Base):
    """
    视图配置表
    """
    __tablename__ = "view_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    view_id: Mapped[str] = mapped_column(String(50), default="", nullable=False, comment="视图唯一标识")
    version: Mapped[int] = mapped_column(Integer, default=10000, nullable=False, comment="视图版本")
    query_id: Mapped[str] = mapped_column(String(50), default=1000, nullable=False, comment="查询ID")
    query_version: Mapped[int] = mapped_column(Integer, default=1000, nullable=False, comment="查询版本")
    status: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False, comment="状态：1-启用 0-禁用") 
    description: Mapped[str] = mapped_column(String(200), default="", nullable=True, comment="视图描述")
    
    __table_args__ = (
        Index("idx_view_version", "view_id", "version"),
    )