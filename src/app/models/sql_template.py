from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Index

class SqlTemplate(Base):
    
    __tablename__ = "sql_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    query_id: Mapped[str] = mapped_column(String(50), nullable=False, default="", comment="查询ID")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default="", comment="版本号")
    query: Mapped[str] = mapped_column(String(255), nullable=False, default="", comment="查询sql")
    query_ext1: Mapped[str] = mapped_column(String(255), nullable=False, default="", comment="扩展sql")
    query_ext2: Mapped[str] = mapped_column(String(255), nullable=False, default="", comment="扩展sql2")

    __table_args__ = (
        Index("idx_query_version", "query_id", "version"),
    )