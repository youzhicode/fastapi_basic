from fastapi import APIRouter

from app.utils.reponse import success

router = APIRouter()


@router.get("/hello")
async def hello_demo():
    """简单测试接口"""
    return success(data="Hello FastAPI Demo API")


@router.get("/info")
async def demo_info():
    """返回示例结构化数据"""
    data = {
        "framework": "FastAPI Base",
        "python_version": "3.14",
        "feature": ["统一返回格式", "全局异常", "JWT鉴权", "SQLAlchemy ORM"]
    }
    return success(data=data, msg="获取框架信息成功")