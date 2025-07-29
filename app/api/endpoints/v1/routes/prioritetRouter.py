from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.services.prioritetService import (
    create_prioritet,
    get_prioritet_by_code,
)

router = APIRouter()

@router.post("/create")
async def create_prioritet_endpoint(request: Request, db: Session = Depends(get_db)):
    return await create_prioritet(request, db)

@router.get("/{prioritet_code}")
async def get_prioritet_by_code_endpoint(prioritet_code: str, db: Session = Depends(get_db)):
    return await get_prioritet_by_code(prioritet_code, db)
