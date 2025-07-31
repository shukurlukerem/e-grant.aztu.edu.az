from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db  
from app.api.endpoints.v1.schemas.prioritetSchema import PrioritetCreate
from app.utils.jwt_required import token_required
from app.services.prioritetService import (
    create_prioritet_service,
    get_prioritet_by_code_service,
)

router = APIRouter()


@router.post("/create-prioritet")
def create_prioritet(prioritet_data: PrioritetCreate, db: Session = Depends(get_db)):
    return create_prioritet_service(prioritet_data.dict(), db)


@router.get("/{prioritet_code}")
def get_prioritet_by_code(prioritet_code: str, db: Session = Depends(get_db)):
    return get_prioritet_by_code_service(prioritet_code, db)
