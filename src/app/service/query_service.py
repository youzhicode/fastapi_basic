import re
from sqlalchemy.orm import Session
from app.curd.query import get_view,get_sql
from app.core.exceptions import QueryException

class QueryService:
    """
    通用查询service
    """
    @staticmethod
    def query(db: Session, view_id: str, version: int, params: dict = None):
        """
        执行通用查询
        """
        if view_id == None or version == None:
            raise QueryException(message="未找到查询视图")
        view_config = get_view(db, view_id, version)
        if view_config == None:
            raise QueryException(message="未找到查询视图")
        
        sql_template = get_sql(db, view_config.query_id, view_config.version)
        if sql_template == None or sql_template.query == '' or sql_template.query == None:
            raise QueryException(message="未找到查询语句配置")
        
        # 拼接sql
        query = sql_template.query
        if sql_template.query_ext1 and sql_template.query_ext1.strip():
            query += sql_template.query_ext1

        if sql_template.query_ext2 and sql_template.query_ext2.strip():
            query += sql_template.query_ext2

        matchs = re.finditer(r":(\w+)", query)

        real_param = params["data"]

        for item in matchs:
            key = item.group(1)
            if key in real_param:
                if isinstance(real_param[key], list):
                    pass
                else:
                    query = re.sub(f"(:{key}\\b)", "?", query)
                

        return query

        


