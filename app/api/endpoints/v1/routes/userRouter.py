from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.endpoints.v1.schemas.userSchema import UserProfileUpdate
from app.services.userService import get_user_by_fin, update_user_profile
from app.utils.jwt_required import token_required as jwt_required

router = APIRouter()

@router.get("/{fin_kod}", dependencies=[Depends(jwt_required([0, 1, 2]))])
def get_profile(fin_kod: str, db: Session = Depends(get_db)):
    user = get_user_by_fin(db, fin_kod)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User found successfully", "data": user.__dict__}

@router.get("/image/{fin_kod}", dependencies=[Depends(jwt_required([0, 1, 2]))])
def get_profile_image(fin_kod: str, db: Session = Depends(get_db)):
    user = get_user_by_fin(db, fin_kod)
    if not user or not user.image:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "User image found successfully", "image_base64": user.image.decode()}

@router.post("/approve", dependencies=[Depends(jwt_required([0, 1, 2]))])
async def complete_profile(
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
    db: Session = Depends(get_db)
):
    image_bytes = await image.read()
    
    profile_data = UserProfileUpdate(
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
    )
    
    updated_user = update_user_profile(db, profile_data, image_bytes)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Profile completed successfully"}
