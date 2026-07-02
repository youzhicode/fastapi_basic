from pydantic import BaseModel

class ParamsModel(BaseModel):
    data: dict = {}

class Query(BaseModel):
    view_id: str
    version: int
    params: ParamsModel | None = ParamsModel(data={})