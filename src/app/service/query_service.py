import re
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.curd.query import get_view,get_sql
from app.core.exceptions import QueryException
from app.utils.logger import log

class QueryService:
    """
    通用查询service, 通用查询，建议只用于列表的查询
    """
    @staticmethod
    def query(db: Session, view_id: str, version: int, params: dict = None):
        """
        执行通用查询
        """
        if view_id is None or version is None:
            raise QueryException(message="未找到查询视图")
        
        view_config = get_view(db, view_id, version)
        if view_config is None:
            raise QueryException(message="未找到查询视图")
        
        sql_template = get_sql(db, view_config.query_id, view_config.version)
        if sql_template is None or sql_template.query is None or sql_template.query == '':
            raise QueryException(message="未找到查询语句配置")
        
        # 拼接sql
        query = sql_template.query
        if sql_template.query_ext1 and sql_template.query_ext1.strip():
            query += sql_template.query_ext1
        
        if sql_template.query_ext2 and sql_template.query_ext2.strip():
            query += sql_template.query_ext2

        log.info(f"查询视图: {view_id}, 版本: {version}, SQL: {query}, 参数: {params}")
        
        # 获取真实参数
        real_param = params.data if params else {}
        
        values = {}
        processed_keys = set()
        
        def replacer(match):
            key = match.group(1)
            
            if key not in real_param:
                return match.group(0)
            
            param_value = real_param[key]
            
            if isinstance(param_value, list):
                # 如果列表为空，返回 NULL（避免 SQL 语法错误）
                if not param_value:
                    return "NULL"
                
                if key in processed_keys:
                    placeholders = [f":{key}{i}" for i in range(len(param_value))]
                    return ",".join(placeholders)
                
                # 首次处理这个 key，生成占位符并收集参数
                placeholders = []
                for i, val in enumerate(param_value):
                    placeholder = f":{key}{i}"
                    placeholders.append(placeholder)
                    values[placeholder[1:]] = val  # 去掉冒号作为字典 key
                
                # 标记为已处理
                processed_keys.add(key)
                return ",".join(placeholders)
            
            else:
                values[key] = param_value
                processed_keys.add(key)
                return f":{key}"
        
        # 执行替换
        expanded_query = re.sub(r":(\w+)", replacer, query)
        log.info(f"展开后的SQL: {expanded_query}, 参数: {values}")
        # 执行查询
        try:
            res = db.execute(text(expanded_query), values).mappings().fetchall()
            data = [dict(row) for row in res]
            return data
        except Exception as e:
            raise QueryException(message=f"查询执行失败: {str(e)}")
        


