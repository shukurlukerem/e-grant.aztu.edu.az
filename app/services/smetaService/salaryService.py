from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.smetaModels.salaryModel import Salary
from app.models.smetaModels.smetaModel import Smeta
from app.models.projectModel import Project
from app.models.userModel import User
from app.models.collabaratorModel import Collaborator
from app.api.endpoints.v1.schemas.smetaSchema.salarySchema import SalaryCreateSchema, SalaryUpdateSchema


async def add_salary(data: SalaryCreateSchema, db: AsyncSession):
    salary_per_month = data.salary_per_month
    months = data.months
    total_salary = salary_per_month * months

    new_salary = Salary(
        project_code=data.project_code,
        fin_kod=data.fin_kod,
        salary_per_month=salary_per_month,
        months=months,
        total_salary=total_salary
    )

    result = await db.execute(select(Smeta).filter_by(project_code=str(data.project_code)))
    main_smeta = result.scalars().first()

    if not main_smeta:
        main_smeta = Smeta(project_code=str(data.project_code))
        db.add(main_smeta)

    main_smeta.total_salary = total_salary

    db.add(new_salary)
    await db.commit()
    await db.refresh(new_salary)
    return new_salary


async def get_salary_smeta_by_project_code(project_code: int, db: AsyncSession):
    result = await db.execute(select(Project).filter_by(project_code=project_code))
    project = result.scalars().first()
    if not project:
        return None

    owner_user = await db.execute(select(User).filter_by(fin_kod=project.fin_kod))
    project_owner_user = owner_user.scalars().first()

    owner_salary = await db.execute(select(Salary).filter_by(project_code=project_code, fin_kod=project.fin_kod))
    project_owner_salary = owner_salary.scalars().first()

    collaborators = await db.execute(select(Collaborator).filter_by(project_code=project_code))
    collaborators = collaborators.scalars().all()

    collaborator_data = []
    for col in collaborators:
        user = await db.execute(select(User).filter_by(fin_kod=col.fin_kod))
        user = user.scalars().first()
        salary = await db.execute(select(Salary).filter_by(project_code=project_code, fin_kod=col.fin_kod))
        salary = salary.scalars().first()

        collaborator_data.append({
            "fin_kod": col.fin_kod,
            "name": user.name if user else None,
            "surname": user.surname if user else None,
            "father_name": user.father_name if user else None,
            "salary": salary.salary_details() if salary else None
        })

    return {
        "project_owner": {
            "fin_kod": project.fin_kod,
            "name": project_owner_user.name if project_owner_user else None,
            "surname": project_owner_user.surname if project_owner_user else None,
            "father_name": project_owner_user.father_name if project_owner_user else None,
            "salary": project_owner_salary.salary_details() if project_owner_salary else None,
        },
        "collaborators": collaborator_data
    }


async def get_all_salaries(db: AsyncSession):
    result = await db.execute(select(Salary))
    return result.scalars().all()


async def update_salary(project_code: int, data: SalaryUpdateSchema, db: AsyncSession):
    result = await db.execute(select(Salary).filter_by(project_code=project_code, fin_kod=data.fin_kod))
    salary = result.scalars().first()

    if not salary:
        return None

    if data.salary_per_month is not None:
        salary.salary_per_month = data.salary_per_month
    if data.months is not None:
        salary.months = data.months

    salary.total_salary = salary.salary_per_month * salary.months

    await db.commit()
    await db.refresh(salary)
    return salary


async def delete_salary(project_code: int, db: AsyncSession):
    result = await db.execute(select(Salary).filter_by(project_code=project_code))
    salary = result.scalars().first()

    if not salary:
        return None

    await db.delete(salary)
    await db.commit()
    return True
