from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash

def get_user_by_username(db: Session, username: str):
    """根据账号查询用户"""
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str):
    """新建用户"""
    hash_pwd = get_password_hash(password)
    db_user = User(username=username, password_hash=hash_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user