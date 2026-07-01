from pydantic import BaseModel

class Query(BaseModel):
    view_id: str
    version: int
    params: dict