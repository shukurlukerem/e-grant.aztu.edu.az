from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db  
from app.api.endpoints.v1.schemas.prioritetSchema import PrioritetCreate
from app.utils.jwt_required import token_required
from app.services.prioritetService import (
    create_prioritet_service,
    get_prioritet_by_code_service,
)
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/create-prioritet")
async def create_prioritet(prioritet_data: PrioritetCreate, db: AsyncSession = Depends(get_db)):
    return await create_prioritet_service(prioritet_data.dict(), db)


@router.get("/priotet/{prioritet_code}")
async def get_prioritet_by_code(prioritet_code: str, db: AsyncSession = Depends(get_db)):
    return await get_prioritet_by_code_service(prioritet_code, db)
