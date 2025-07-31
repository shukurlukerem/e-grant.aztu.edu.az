from app.db.session import get_db
from fastapi import Depends, status
from sqlalchemy.future import select
from app.models.authModel import Auth
from app.models.userModel import User
from app.models.projectModel import Project
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.jwt_util import encode_auth_token
from app.models.collabaratorModel import Collaborator
from app.api.endpoints.v1.schemas.auth import SignIn, SignUp
from app.utils.password import hash_password, verify_password

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def signup(
    signup_details: SignUp,
    db: AsyncSession = Depends(get_db)
):
    try:
        fetched_data = await db.execute(
            select(Auth)
            .where(Auth.fin_kod == signup_details.fin_kod)
        )

        exist_user = fetched_data.scalar_one_or_none()

        if exist_user:
            return JSONResponse(
                content={
                    "statusCode": 409,
                    "message": "Fin kod already exists."
                }
            )
        
        new_auth_user = Auth(
            fin_kod=signup_details.fin_kod,
            user_type=signup_details.user_type,
            project_role=signup_details.project_role,
            password_hash=hash_password(signup_details.password),
            approved=False
        )

        # new_user = User()

        db.add(new_auth_user)
        db.commit()
        db.refresh(new_auth_user)

        return JSONResponse(
            content={
                "statusCode": 201,
                "message": "User created"
            }, status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "statusCode": 500,
                "error": 500
            }
        )
    
async def signin(
    signin_details: SignIn,
    db: AsyncSession = Depends(get_db)
):
    try:
        fetched_data = await db.execute(
            select(Auth)
            .where(Auth.fin_kod == signin_details.fin_kod)
        )

        user = fetched_data.scalar_one_or_none()

        if not user or not verify_password(signin_details.password, user.password_hash):
            return JSONResponse(
                content={
                    "statusCode": 401,
                    "message": "UNAUTHORIZED"
                }, status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        collaborator_data = await db.execute(
            select(Collaborator)
            .where(Collaborator.fin_kod == user.fin_kod)
        )

        collaborator = collaborator_data.scalar_one_or_none()

        project_data = await db.execute(
            select(Project)
            .where(Project.fin_kod == user.fin_kod)
        )

        project = project_data.scalar_one_or_none()

        is_collaborator = True if collaborator else False

        project_code = collaborator.project_code if collaborator and collaborator.project_code is not None \
               else (project.project_code if project and project.project_code is not None else None)


        user_data = await db.execute(
            select(User)
            .where(User.fin_kod == user.fin_kod)
        )

        profile = user_data.scalar_one_or_none()

        profile_completed = True if profile.profile_completed else False

        token = encode_auth_token(user.id, user.fin_kod, profile_completed, role=user.project_role) 

        return JSONResponse(
            content={
                "statusCode": 200,
                "message": "AUTHORIZED",
                "data": {
                    "fin_kod": user.fin_kod,
                    "project_role": user.project_role,
                    "project_code": project_code,   
                    "profile_completed": profile_completed,
                    "is_collaborator": is_collaborator
                },
                "token": token
            }
        )

    except Exception as e:
        logger.error(f"Error in signin: {e}", exc_info=True)
        return JSONResponse(
            content={
                "statusCode": 500,
                "error": str(e)
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )