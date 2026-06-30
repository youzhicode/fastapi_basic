import time
from typing import Callable
from fastapi import Request
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from app.utils.logger import log
from app.core.config import settings

# 无需Token校验的白名单路径
AUTH_WHITE_LIST = [
    "/",
    "/api/v1/auth/login",
    "/docs",
    "/redoc",
    "/openapi.json",
]

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        # 请求信息
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"

        log.info(f"收到请求 | IP:{client_ip} | {method} {url}")

        response = await call_next(request)

        # 计算耗时
        cost_ms = round((time.time() - start_time) * 1000, 2)
        status_code = response.status_code

        log.info(f"请求完成 | Status:{status_code} | 耗时:{cost_ms}ms | {method} {url}")
        return response


# 全局Token鉴权拦截中间件
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path

        # 白名单直接放行，跳过token校验
        if path in AUTH_WHITE_LIST:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        # 1. 无Authorization头
        if not auth_header:
            log.warning(f"{path} 未携带Authorization请求头")
            raise HTTPException(status_code=401, detail="登录凭证缺失，请重新登录")

        header_arr = auth_header.split(" ")
        # 2. 格式校验 Bearer xxx
        if len(header_arr) != 2 or header_arr[0].lower() != "bearer":
            log.warning(f"{path} token格式错误：{auth_header}")
            raise HTTPException(status_code=401, detail="凭证格式错误，标准格式：Bearer token字符串")

        token = header_arr[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("sub")
            if not user_id:
                raise ValueError("token载荷sub为空")
            # 将登录用户id挂载到request，所有接口可直接取
            request.state.user_id = user_id
        except JWTError:
            log.warning(f"{path} token失效或非法")
            raise HTTPException(status_code=401, detail="登录凭证已过期或无效，请重新登录")
        except Exception as err:
            log.error(f"{path} 鉴权异常：{str(err)}")
            raise HTTPException(status_code=401, detail="身份校验失败")

        return await call_next(request)