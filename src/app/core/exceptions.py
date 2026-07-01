from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import log
from app.utils.reponse import fail
from typing import Optional, Any


class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as exc:
            # 直接使用异常自带的detail，不再统一覆盖
            log.warning(f"HTTP异常 code:{exc.status_code} msg:{exc.detail}")
            return JSONResponse(
                content=fail(code=exc.status_code, msg=exc.detail).model_dump()
            )
        except Exception as exc:
            log.opt(exception=True).error(f"系统未知异常：{str(exc)}")
            return JSONResponse(
                content=fail(code=500, msg="服务器内部错误").model_dump()
            )
        
async def validation_exception_handler(request, exc: RequestValidationError):
    log.warning(f"参数验证失败: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=fail(code=422, msg="请求参数错误，请检查必填字段").model_dump()
    )


class AppException(Exception):
    """应用基础异常"""
    def __init__(self, code: int = 500, message: str = "系统异常"):
        self.code = code
        self.message = message
        super.__init__(message)


class QueryException(AppException):
    """
    通用查询异常
    """
    def __init__(self, code = 500, message = "通用查询异常"):
        super().__init__(code, message)