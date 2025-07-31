import base64
import logging
from datetime import datetime
from app.db.session import get_db
from fastapi import Depends, status
from sqlalchemy.future import select
from app.models.userModel import User
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.endpoints.v1.schemas.userSchema import CreateUser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def get_profile(
    fin_kod: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(User)
            .where(User.fin_kod == fin_kod)
        )

        user = result.scalar_one_or_none()

        if not user:
            return JSONResponse(
                content={
                    "statusCode": 404,
                    "message": "No user found."
                }, status_code=status.HTTP_404_NOT_FOUND
            )
        
        return JSONResponse(
            content={
                "statusCode": 200,
                "message": "User fetched successfully.",
                "data": user.to_dict()
            }, status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        logger.error(f"Unexpected error completing profile: {e}", exc_info=True)
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def complete_profile(
    user_details: CreateUser,
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.debug(f"Starting complete_profile for fin_kod={user_details.fin_kod}")

        result = await db.execute(select(User).where(User.fin_kod == user_details.fin_kod))
        user = result.scalar_one_or_none()

        if not user:
            logger.info(f"User not found with fin_kod={user_details.fin_kod}")
            return JSONResponse(
                content={"error": "User not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )

        logger.debug("User found in database")

        try:
            image_bytes = await user_details.image.read()
            logger.debug(f"Read image bytes: {len(image_bytes)} bytes")
        except Exception as e:
            logger.warning(f"Image read error: {e}", exc_info=True)
            return JSONResponse(
                content={"error": "Could not read image file"},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Assign fields, log a few for debugging
        user.name = user_details.name
        user.surname = user_details.surname
        user.father_name = user_details.father_name
        user.image = image_bytes
        # (Log only a few fields to avoid clutter)
        logger.debug(f"Assigned user name: {user.name}, surname: {user.surname}")

        try:
            if user_details.scientific_date:
                user.scientific_date = datetime.strptime(user_details.scientific_date, "%Y-%m-%d")
                logger.debug(f"Parsed scientific_date: {user.scientific_date}")
            else:
                user.scientific_date = None
        except ValueError as ve:
            logger.warning(f"Invalid scientific_date format: {user_details.scientific_date}", exc_info=True)
            return JSONResponse(
                content={"error": "Invalid scientific_date format. Use YYYY-MM-DD."},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        try:
            if user_details.scientific_name_date:
                user.scientific_name_date = datetime.strptime(user_details.scientific_name_date, "%Y-%m-%d")
                logger.debug(f"Parsed scientific_name_date: {user.scientific_name_date}")
            else:
                user.scientific_name_date = None
        except ValueError as ve:
            logger.warning(f"Invalid scientific_name_date format: {user_details.scientific_name_date}", exc_info=True)
            return JSONResponse(
                content={"error": "Invalid scientific_name_date format. Use YYYY-MM-DD."},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        user.profile_completed = True

        logger.debug("Committing changes to database")
        await db.commit()
        logger.info(f"Profile completed for user with fin_kod={user_details.fin_kod}")

        # Encode image bytes for safe JSON returning
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        logger.debug("Encoded image bytes to base64 string")

        return JSONResponse(
            content={
                "message": "Profile completed successfully.",
                "image_base64": encoded_image
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Unexpected error completing profile: {e}", exc_info=True)
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
