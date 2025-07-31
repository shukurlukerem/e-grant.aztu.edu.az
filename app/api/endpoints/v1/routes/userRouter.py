import logging
from app.services.userService import *
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.endpoints.v1.schemas.userSchema import UserBase, CreateUser
from app.utils.jwt_required import token_required as jwt_required

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/profile/{fin_kod}")
async def get_user_endpoint(
    fin_kod: str,
    db: AsyncSession = Depends(get_db)
):
    return await get_profile(fin_kod, db)

@router.post("/approve/profile")
async def app_profile_endpoint(
    fin_kod: str = Form(...),
    name: str = Form(...),
    surname: str = Form(...),
    father_name: str = Form(...),
    born_place: str = Form(...),
    living_location: str = Form(...),
    home_phone: str = Form(...),
    personal_mobile_number: str = Form(...),
    personal_email: str = Form(...),
    citizenship: str = Form(...),
    personal_id_number: str = Form(...),
    sex: str = Form(...),
    work_place: str = Form(...),
    department: str = Form(...),
    duty: str = Form(...),
    main_education: str = Form(...),
    additonal_education: str = Form(None),
    scientific_degree: str = Form(None),
    scientific_date: str = Form(None),
    scientific_name: str = Form(None),
    scientific_name_date: str = Form(None),
    work_location: str = Form(None),
    work_phone: str = Form(None),
    work_email: str = Form(None),
    born_date: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    # Build the CreateUser model manually:
    user_details = CreateUser(
        fin_kod=fin_kod,
        name=name,
        surname=surname,
        father_name=father_name,
        born_place=born_place,
        living_location=living_location,
        home_phone=home_phone,
        personal_mobile_number=personal_mobile_number,
        personal_email=personal_email,
        citizenship=citizenship,
        personal_id_number=personal_id_number,
        sex=sex,
        work_place=work_place,
        department=department,
        duty=duty,
        main_education=main_education,
        additonal_education=additonal_education,
        scientific_degree=scientific_degree,
        scientific_date=scientific_date,
        scientific_name=scientific_name,
        scientific_name_date=scientific_name_date,
        work_location=work_location,
        work_phone=work_phone,
        work_email=work_email,
        born_date=born_date,
        image=image
    )
    return await complete_profile(user_details, db)