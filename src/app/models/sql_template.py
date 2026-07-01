from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Index

"""
CREATE TABLE `sql_templates` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `view_id` VARCHAR(50) NOT NULL COMMENT '视图唯一标识',
    `version` INT NOT NULL DEFAULT 1 COMMENT '版本号',
    `sql_template` TEXT NOT NULL COMMENT 'SQL模板，使用:column占位符',
    `description` VARCHAR(200) COMMENT '版本描述',
    `is_active` TINYINT DEFAULT 1 COMMENT '是否激活：1-是 0-否',
    `created_by` VARCHAR(50) COMMENT '创建人'
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_view_version` (`view_id`, `version`),
    INDEX `idx_view_active` (`view_id`, `is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='SQL模板版本表';
"""

class SqlTemplate(Base):
    
    __tablename__ = "sql_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    query_id: Mapped[int] = mapped_column(Integer, nullable=False, default="", comment="查询ID")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default="", comment="版本号")
    query: Mapped[str] = mapped_column(String(255), nullable=False, default="", comment="查询sql")
    query_ext1: Mapped[str] = mapped_column(String(255), nullable=False, default="", comment="扩展sql")
    query_ext2: Mapped[str] = mapped_column(String(255), nullable=False, default="", comment="扩展sql2")

    __table_args__ = (
        Index("idx_query_version", "query_id", "version"),
    )