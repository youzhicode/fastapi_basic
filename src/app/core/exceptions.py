from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import log
from app.utils.reponse import fail


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