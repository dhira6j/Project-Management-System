from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional # Added Optional

from .. import crud, schemas, models
from ..database import get_db
from ..dependencies.auth import get_current_active_user, get_project_manager_user, get_admin_user

router = APIRouter()

@router.post("/", response_model=schemas.Project, dependencies=[Depends(get_project_manager_user)])
def create_new_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    if current_user.role == models.user.UserRole.PROJECT_MANAGER and project.project_manager_id is None:
        project.project_manager_id = current_user.id
    elif project.project_manager_id and project.project_manager_id != current_user.id and current_user.role != models.user.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Project Managers can only assign projects to themselves unless Admin.")
    return crud.project.create_project(db=db, project=project)

@router.get("/", response_model=List[schemas.Project])
def read_all_projects(
    skip: int = 0, limit: int = 100, search: Optional[str] = None, # Added search
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    projects = crud.project.get_projects(db, skip=skip, limit=limit, search=search) # Pass search
    return projects

@router.get("/{project_id}", response_model=schemas.ProjectWithDetails)
def read_single_project(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_project = crud.project.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=schemas.Project)
def update_existing_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_project = crud.project.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    is_admin = current_user.role == models.user.UserRole.ADMIN
    is_pm_of_project = db_project.project_manager_id == current_user.id
    if not (is_admin or (current_user.role == models.user.UserRole.PROJECT_MANAGER and is_pm_of_project)):
        raise HTTPException(status_code=403, detail="Not authorized to update this project. Must be Admin or the assigned Project Manager.")
    return crud.project.update_project(db=db, db_project=db_project, project_in=project)

@router.delete("/{project_id}", response_model=schemas.Project)
def delete_single_project(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_project = crud.project.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    is_admin = current_user.role == models.user.UserRole.ADMIN
    is_pm_of_project = db_project.project_manager_id == current_user.id
    if not (is_admin or (current_user.role == models.user.UserRole.PROJECT_MANAGER and is_pm_of_project)):
        raise HTTPException(status_code=403, detail="Not authorized to delete this project. Must be Admin or the assigned Project Manager.")
    return crud.project.delete_project(db=db, db_project=db_project)
