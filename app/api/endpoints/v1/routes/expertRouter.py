from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
from app.db.session import get_db
from app.api.endpoints.v1.schemas.expertSchema import ExpertCreate
from app.services.expertService import create_expert, set_expert, get_experts

router = APIRouter()

@router.post("/create-expert", dependencies=[Depends(RateLimiter(times=100, seconds=60))])
async def create_expert_endpoint(request: Request, db: Session = Depends(get_db)):
    return await create_expert(request, db)

@router.post("/set-expert", dependencies=[Depends(RateLimiter(times=100, seconds=60))])
async def set_expert_endpoint(request: Request, db: Session = Depends(get_db)):
    return await set_expert(request, db)

@router.get("/experts")
async def get_experts_endpoint(db: Session = Depends(get_db)):
    return await get_experts(db)