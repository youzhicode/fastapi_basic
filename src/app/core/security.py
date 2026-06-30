from datetime import datetime, timedelta, UTC
from typing import Any, Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Any, expires_delta: Optional[timedelta] = None) -> str:
    """生成JWT访问令牌"""
    to_encode = {"sub": str(subject)}
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验明文密码与哈希密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """密码哈希加密"""
    return pwd_context.hash(password)