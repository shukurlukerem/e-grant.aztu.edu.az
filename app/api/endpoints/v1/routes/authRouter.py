from app.services.auth import *
from app.db.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.endpoints.v1.schemas.auth import SignIn, SignUp

router = APIRouter()

@router.post("/signin")
async def signin_endpoint(
    signin_details: SignIn,
    db: AsyncSession = Depends(get_db)
):
    return await signin(signin_details, db)

@router.post("/signup")
async def signup_endpoint(
    signup_details: SignUp,
    db: AsyncSession = Depends(get_db)
):
    return await signup(signup_details, db)