from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import GlobalExceptionMiddleware,validation_exception_handler
from app.core.middleware import RequestLogMiddleware, AuthMiddleware
from app.core.config import settings
from app.api import api_v1


def create_app() -> FastAPI:

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="通用FastAPI基础脚手架，支持复用快速搭建新项目"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    # 全局鉴权拦截
    app.add_middleware(AuthMiddleware)
    # 记录请求日志中间件
    app.add_middleware(RequestLogMiddleware)
    # 全局异常捕获中间件
    app.add_middleware(GlobalExceptionMiddleware)
    app.include_router(api_v1, prefix="/api/v1")

        # 根路径健康检查
    @app.get("/")
    async def root():
        return {"msg": "FastAPI Base Framework Running", "env": settings.APP_ENV}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_ENV == "dev"
    )