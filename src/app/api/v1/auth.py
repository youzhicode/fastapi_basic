from fastapi import APIRouter, Depends, Request
from app.schemas.auth import LoginReq
from app.utils.reponse import success
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.service.admin_service import AdminService

router = APIRouter()

@router.post("/login")
def login(req: LoginReq, db: Session = Depends(get_db)):
    access_token = AdminService.login(db, req.username, req.password)
    return success(data={"access_token": access_token, "token_type": "bearer"})


@router.get("/me")
def get_login_info(request: Request):
    """需要token鉴权，获取当前登录用户"""
    user_id = request.state.user_id
    return success(data={"user_id": user_id, "msg": "认证通过"})