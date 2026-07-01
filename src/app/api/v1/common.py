from fastapi import Depends, APIRouter
from app.schemas.common import Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.reponse import success, fail
from app.service.query_service import QueryService

router = APIRouter()

@router.post("/query")
def commond_query(query: Query, db: Session = Depends(get_db)):
    return success(data=QueryService.query(db, query.view_id, query.version, query.params))