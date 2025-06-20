from sqlalchemy.orm import Session
from sqlalchemy import or_ # For searching multiple fields
from typing import Optional # For Optional search parameter
from .. import models, schemas

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None): # Added search
    query = db.query(models.Project)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Project.title.ilike(search_term),
                models.Project.description.ilike(search_term)
            )
        )
    return query.offset(skip).limit(limit).all()

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict()) # pydantic v2: model_dump()
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, db_project: models.Project, project_in: schemas.ProjectUpdate):
    project_data = project_in.dict(exclude_unset=True) # pydantic v2: model_dump()
    for key, value in project_data.items():
        setattr(db_project, key, value)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, db_project: models.Project):
    db.delete(db_project)
    db.commit()
    return db_project
