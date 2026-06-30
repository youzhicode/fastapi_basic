from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.curd.admin import get_admin_by_username
from app.core.security import verify_password, create_access_token, get_password_hash
from app.utils.logger import log


class AdminService:

    @staticmethod
    def login(db: Session, username: str, password: str):
        """
            用户登录认证
        """
        admin = get_admin_by_username(db, username=username)
        if not admin:
            raise HTTPException(status_code=400, detail="账号不存在")
        
        if not verify_password(password, admin.password_hash):
            raise HTTPException(status_code=400, detail="密码错误")
        token = create_access_token(subject=admin.id)
        return token
        

        