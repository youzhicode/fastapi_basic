from sqlalchemy.orm import Session
from app.models.view_config import ViewConfig
from app.models.sql_template import SqlTemplate
from app.enum import ViewStatusEnum

def get_view(db: Session, view_id: str, version: int) -> ViewConfig | None:
    """
    获取视图配置
    """
    return (
        db.query(ViewConfig)
        .filter(ViewConfig.view_id == view_id)
        .filter(ViewConfig.version == version)
        .filter(ViewConfig.status == ViewStatusEnum.ENABLE)
        .first()
    )

def get_sql(db: Session, query_id: str, version: int) -> SqlTemplate | None:
    """
    获取查询语句
    """
    return (
        db.query(SqlTemplate)
        .filter(SqlTemplate.query_id == query_id)
        .filter(SqlTemplate.version == version)
        .first()
    )