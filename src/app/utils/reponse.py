from pydantic import BaseModel
from typing import Any, Optional


class ResponseModel(BaseModel):
    code: int
    msg: str
    data: Optional[Any] = None


def success(data: Any = None, msg: str = "操作成功") -> ResponseModel:
    return ResponseModel(code=200, msg=msg, data=data)


def fail(code: int = 400, msg: str = "操作失败", data: Any = None) -> ResponseModel:
    return ResponseModel(code=code, msg=msg, data=data)