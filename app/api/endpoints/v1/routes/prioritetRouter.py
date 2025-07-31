from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.api.endpoints.v1.schemas.prioritetSchema import PrioritetCreate
from app.services.prioritetService import (
    create_prioritet_service,
    get_prioritet_by_code_service
)

router = APIRouter()

@router.post("/create-prioritet")
async def create_prioritet(data: PrioritetCreate):
    print(data.prioritet_name)
    return {"message": "Prioritet created", "prioritet_name": data.prioritet_name}


@router.get("/{prioritet_code}")
async def get_prioritet(prioritet_code: str, db: Session = Depends(get_db)):
    return get_prioritet_by_code_service(prioritet_code, db)
