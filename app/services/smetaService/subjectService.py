from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.projectModel import Project
from app.models.smetaModels.smetaModel import Smeta
from app.models.smetaModels.subjectModel import SubjectOfPurchase
from fastapi import HTTPException
from decimal import Decimal

async def add_subject(data: dict, db: AsyncSession):
    project = await db.execute(select(Project).where(
        Project.project_code == data['project_code'],
        Project.fin_kod == data['fin_code']
    ))
    matching_project = project.scalars().first()
    if not matching_project:
        raise HTTPException(status_code=404, detail="No matching project found with given project_code and fin_code")

    total = data['price'] * data['quantity']

    new_subject = SubjectOfPurchase(
        project_code=data['project_code'],
        equipment_name=data['equipment_name'],
        unit_of_measure=data['unit_of_measure'],
        price=data['price'],
        quantity=data['quantity'],
        total_amount=total
    )

    smeta_result = await db.execute(select(Smeta).where(Smeta.project_code == data['project_code']))
    main_smeta = smeta_result.scalars().first()

    if not main_smeta:
        main_smeta = Smeta(project_code=data['project_code'])
        db.add(main_smeta)

    if main_smeta.total_equipment is None:
        main_smeta.total_equipment = 0

    main_smeta.total_equipment += Decimal(total)

    db.add(new_subject)
    await db.commit()
    return {"message": "Subject added successfully"}

async def get_subjects(project_code: int, db: AsyncSession):
    result = await db.execute(select(SubjectOfPurchase).where(SubjectOfPurchase.project_code == project_code))
    subjects = result.scalars().all()
    return [subject.subject_details() for subject in subjects]

async def update_subject(project_code: int, data: dict, db: AsyncSession):
    result = await db.execute(select(SubjectOfPurchase).where(SubjectOfPurchase.project_code == project_code))
    subject = result.scalars().first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    old_total = subject.total_amount or 0

    for key in ['equipment_name', 'unit_of_measure', 'price', 'quantity']:
        if key in data:
            setattr(subject, key, data[key])

    if 'price' in data or 'quantity' in data:
        subject.total_amount = subject.price * subject.quantity

    difference = subject.total_amount - old_total

    smeta_result = await db.execute(select(Smeta).where(Smeta.project_code == project_code))
    smeta = smeta_result.scalars().first()
    if not smeta:
        smeta = Smeta(project_code=project_code)
        db.add(smeta)

    if smeta.total_equipment is None:
        smeta.total_equipment = 0

    smeta.total_equipment += difference

    await db.commit()
    return {"message": "Subject updated successfully", "data": subject.subject_details()}

async def delete_subject(project_code: int, id: int, db: AsyncSession):
    result = await db.execute(select(SubjectOfPurchase).where(SubjectOfPurchase.id == id))
    subject = result.scalars().first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found with provided project_code")

    smeta_result = await db.execute(select(Smeta).where(Smeta.project_code == project_code))
    smeta = smeta_result.scalars().first()
    if not smeta:
        smeta = Smeta(project_code=project_code)
        db.add(smeta)

    smeta.total_equipment -= subject.total_amount

    await db.delete(subject)
    await db.commit()
    return {"message": "Subject deleted successfully"}
