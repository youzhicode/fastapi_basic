from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from app.core.dependencies import get_current_user
from app.core.security import create_access_token
from app.schemas.auth import LoginReq
from app.utils.reponse import success

router = APIRouter()

@router.post("/login")
def login(req: LoginReq):
    """
    JSON方式登录获取token，请求体为json
    """
    # 模拟用户校验，后续替换数据库查询逻辑
    mock_user_id = "10001"
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(subject=mock_user_id, expires_delta=access_token_expires)
    return success(data={"access_token": access_token, "token_type": "bearer"})


@router.get("/me")
def get_login_info(request: Request):
    """需要token鉴权，获取当前登录用户"""
    user_id = request.state.user_id
    return success(data={"user_id": user_id, "msg": "认证通过"})