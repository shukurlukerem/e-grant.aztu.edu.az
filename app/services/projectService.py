import random
import logging
from app.db.session import get_db
from fastapi import Depends, status
from sqlalchemy.future import select
from app.models.userModel import User
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from app.models.projectModel import Project
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.endpoints.v1.schemas.projectSchema import ProjectCreate, ProjectUpdate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def generate_unique_project_code(db: AsyncSession) -> int:
    while True:
        code = random.randint(10000000, 99999999)
        result = await db.execute(select(Project).filter_by(project_code=code))
        if not result.scalars().first():
            logger.info(f"Generated unique project code: {code}")
            return code


async def create_or_update_project(db: AsyncSession, data: ProjectCreate):
    logger.info(f"Creating or updating project for FIN code: {data.fin_kod}")

    result = await db.execute(select(Project).filter_by(fin_kod=data.fin_kod))
    project = result.scalars().first()

    if not project:
        logger.info("No existing project found. Creating new project.")
        project = Project(
            fin_kod=data.fin_kod,
            project_code=await generate_unique_project_code(db),
            submitted=False,
            submitted_at=datetime.utcnow()
        )
        db.add(project)

    data_dict = data.dict()
    if data_dict.get("project_deadline") and data_dict["project_deadline"].tzinfo:
        data_dict["project_deadline"] = data_dict["project_deadline"].astimezone(timezone.utc).replace(tzinfo=None)

    if data_dict.get("submitted_at") and data_dict["submitted_at"].tzinfo:
        data_dict["submitted_at"] = data_dict["submitted_at"].astimezone(timezone.utc).replace(tzinfo=None)

    for field, value in data_dict.items():
        if hasattr(project, field) and value is not None:
            setattr(project, field, value)

    required_fields = [
        'project_name', 'project_purpose', 'project_annotation',
        'project_key_words', 'project_scientific_idea', 'project_structure',
        'team_characterization', 'project_monitoring', 'project_requirements',
        'project_deadline', 'collaborator_limit', 'max_smeta_amount', 'priotet'
    ]

    all_fields_filled = all(getattr(project, field) for field in required_fields)
    project.approved = 1 if all_fields_filled else 0

    await db.commit()
    await db.refresh(project)

    logger.info(f"Project successfully created/updated for FIN code: {data.fin_kod}")

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({
            "successCode": 201,
            "data": project.project_detail(),
            "message": "Project created/updated successfully"
        })
    )


async def get_all_projects(db: AsyncSession = Depends(get_db)):
    logger.info("Fetching all projects.")
    try:
        result = await db.execute(select(Project))
        projects = result.scalars().all()

        if not projects:
            logger.warning("No projects found in the database.")
            return JSONResponse(
                status_code=204,
                content={"statusCode": 204, "message": "No projects found."}
            )

        project_data = []

        for p in projects:
            user_result = await db.execute(
                select(User.name, User.surname).where(User.fin_kod == p.fin_kod)
            )
            user = user_result.scalar_one_or_none()

            project_detail = p.project_detail()

            # jsonable_encoder converts datetime and other types safely
            project_detail = jsonable_encoder(project_detail)

            project_data.append({
                **project_detail,
                "user": {
                    "name": user.name if user else None,
                    "surname": user.surname if user else None
                }
            })

        logger.info(f"{len(project_data)} projects fetched successfully.")

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({
                "statusCode": 200,
                "message": "Projects fetched successfully.",
                "data": project_data
            })
        )

    except Exception as e:
        logger.error(f"Error fetching projects: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"statusCode": 500, "error": str(e)}
        )

async def get_project_by_code(db: AsyncSession, project_code: int):
    try:
        logger.info(f"Fetching project by project code: {project_code}")
        result = await db.execute(select(Project).filter_by(project_code=project_code))
        project = result.scalar_one_or_none()

        if not project:
            logger.warning(f"Project not found for code: {project_code}")
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Project not found with the provided code."}
            )

        logger.info(f"Project found for code: {project_code}")

        project_data = jsonable_encoder(project.project_detail())

        return JSONResponse(
            status_code=200,
            content={
                "statusCode": 200,
                "message": "Project fetched.",
                "data": project_data
            }
        )
    
    except Exception as e:
        logger.error(f"Error fetching projects: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"statusCode": 500, "error": str(e)}
        )

async def get_project_by_fin_kod(db: AsyncSession, fin_kod: str):
    logger.info(f"Fetching project by FIN code: {fin_kod}")
    result = await db.execute(select(Project).filter_by(fin_kod=fin_kod))
    project = result.scalars().first()
    if not project:
        logger.warning(f"Project not found for FIN code: {fin_kod}")
        return {"success": False, "message": "Project not found with the provided financial code."}
    logger.info(f"Project found for FIN code: {fin_kod}")

    return {
        "success": True,
        "data": project.project_detail(),
        "message": "Project data fetched successfully."
    }


def make_naive_utc(dt):
    if dt and dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

async def update_project(db: AsyncSession, data: ProjectUpdate):
    logger.info(f"Updating project for FIN code: {data.fin_kod}")
    result = await db.execute(select(Project).filter_by(fin_kod=data.fin_kod))
    project = result.scalars().first()
    if not project:
        logger.warning(f"Project to update not found for FIN code: {data.fin_kod}")
        return {"success": False, "message": "Project not found to update."}

    data_dict = data.dict()

    for field, value in data_dict.items():
        if isinstance(value, datetime):
            value = make_naive_utc(value)

        if hasattr(project, field) and value is not None:
            setattr(project, field, value)

    await db.commit()
    await db.refresh(project)

    logger.info(f"Project successfully updated for FIN code: {data.fin_kod}")
    return {
        "success": True,
        "data": project.project_detail(),
        "message": "Project updated successfully"
    }


async def delete_project(db: AsyncSession, fin_kod: str):
    logger.info(f"Deleting project for FIN code: {fin_kod}")
    result = await db.execute(
        select(Project).where(Project.fin_kod == fin_kod)
    )
    project = result.scalar_one_or_none()
    if not project:
        return JSONResponse(
            content={
                "statusCode": 404,
                "message": "Project not found"
            }, status_code=status.HTTP_404_NOT_FOUND
        )

    await db.delete(project)
    await db.commit()

    logger.info(f"Project successfully deleted for FIN code: {fin_kod}")
    return JSONResponse(
            content={
                "statusCode": 200,
                "message": "Project deleted"
            }
        )
