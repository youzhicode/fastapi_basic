from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.reponse import fail


class GlobalExceptionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as exc:
            resp = fail(code=exc.status_code, msg=exc.detail)
            return JSONResponse(content=resp.model_dump(), status_code=200)
        except Exception as exc:
            resp = fail(code=500, msg=f"服务器内部错误: {str(exc)}")
            return JSONResponse(content=resp.model_dump(), status_code=500)