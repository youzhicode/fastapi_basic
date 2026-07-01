from pydantic import BaseModel, Field, field_validator

class LoginReq(BaseModel):
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="用户名"
    )
    password: str = Field(
        ..., 
        min_length=6, 
        max_length=20,
        description="密码"
    )