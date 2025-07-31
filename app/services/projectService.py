from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.projectModel import Project
from app.api.endpoints.v1.schemas.projectSchema import ProjectCreate, ProjectUpdate
from app.utils.jwt_required import token_required
from app.models.userModel import User
import random


async def generate_unique_project_code(db: AsyncSession) -> int:
    while True:
        code = random.randint(10000000, 99999999)
        result = await db.execute(select(Project).filter_by(project_code=code))
        if not result.scalars().first():
            return code


from datetime import datetime, timezone

async def create_or_update_project(db: AsyncSession, data: ProjectCreate):

    result = await db.execute(select(Project).filter_by(fin_kod=data.fin_kod))
    project = result.scalars().first()

    if not project:
        project = Project(
            fin_kod=data.fin_kod,
            project_code=await generate_unique_project_code(db),
            submitted=False,
            submitted_at=datetime.utcnow() 
        )
        db.add(project)

    # Clean tz-aware datetime fields
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

    return {
        "success": True,
        "data": project.project_detail(),
        "message": "Project created/updated successfully"
    }



async def get_all_projects(db: AsyncSession):
    result = await db.execute(select(Project))
    projects = result.scalars().all()

    if not projects:
        return JSONResponse(content={
            "statusCode": 204,
            "message": "No projects found."
        })

    project_data = []

    for p in projects:
        user_result = await db.execute(
            select(User.name, User.surname).where(User.fin_kod == p.fin_kod)
        )
        user = user_result.first()

        project_data.append({
            **p.project_detail(),
            "user": {
                "name": user.name if user else None,
                "surname": user.surname if user else None
            }
        })

    return JSONResponse(
        content={
            "statusCode": 200,
            "message": "Project fetched successfully.",
            "data": project_data
        }
    )


async def get_project_by_code(db: AsyncSession, project_code: int):
    result = await db.execute(select(Project).filter_by(project_code=project_code))
    project = result.scalars().first()
    if not project:
        return {"success": False, "message": "Project not found with the provided code."}
    return {
        "success": True,
        "data": project.project_detail()
    }


async def get_project_by_fin_kod(db: AsyncSession, fin_kod: str):
    result = await db.execute(select(Project).filter_by(fin_kod=fin_kod))
    project = result.scalars().first()
    if not project:
        return {"success": False, "message": "Project not found with the provided financial code."}
    return {
        "success": True,
        "data": project.project_detail(),
        "message": "Project data fetched successfully."
    }


async def update_project(db: AsyncSession, data: ProjectUpdate):
    result = await db.execute(select(Project).filter_by(fin_kod=data.fin_kod))
    project = result.scalars().first()
    if not project:
        return {"success": False, "message": "Project not found to update."}

    for field, value in data.dict().items():
        if hasattr(project, field) and value is not None:
            setattr(project, field, value)

    await db.commit()
    await db.refresh(project)

    return {
        "success": True,
        "data": project.project_detail(),
        "message": "Project updated successfully"
    }


async def delete_project(db: AsyncSession, fin_kod: str):
    result = await db.execute(select(Project).filter_by(fin_kod=fin_kod))
    project = result.scalars().first()
    if not project:
        return {"success": False, "message": "Project not found to delete."}

    await db.delete(project)
    await db.commit()

    return {
        "success": True,
        "message": "Project deleted successfully"
    }
