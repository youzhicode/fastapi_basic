from fastapi import APIRouter
from app.api.v1.demo import router as demo_router
from app.api.v1.auth import router as auth_router
from app.api.v1.common import router as common_router

api_v1 = APIRouter()
api_v1.include_router(demo_router, prefix="/demo", tags=["演示接口"])
api_v1.include_router(auth_router, prefix="/auth", tags=["登录验证"])
api_v1.include_router(common_router, prefix="/common", tags=["通用模块"])

