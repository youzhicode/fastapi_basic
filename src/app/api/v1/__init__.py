from fastapi import APIRouter
from app.api.v1.demo import router as demo_router

api_v1 = APIRouter()
api_v1.include_router(demo_router, prefix="/demo", tags=["演示接口"])
