from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, models
from ..database import get_db
from ..dependencies.auth import get_current_active_user, get_project_manager_user, get_consultant_user, get_admin_user

router = APIRouter()

@router.post("/", response_model=schemas.Deliverable) # PMs or Admins can create
def create_new_deliverable(deliverable: schemas.DeliverableCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_project_manager_user)): # Ensures PM or Admin
    project = crud.project.get_project(db, project_id=deliverable.project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {deliverable.project_id} not found")

    is_admin = current_user.role == models.user.UserRole.ADMIN
    is_pm_of_project = project.project_manager_id == current_user.id

    if not (is_admin or (current_user.role == models.user.UserRole.PROJECT_MANAGER and is_pm_of_project)):
        raise HTTPException(status_code=403, detail="Not authorized to create deliverables for this project.")

    # Check if assigned_consultant_id is valid user with consultant role
    if deliverable.assigned_consultant_id:
        consultant_user = crud.user.get_user(db, user_id=deliverable.assigned_consultant_id)
        if not consultant_user or consultant_user.role != models.user.UserRole.CONSULTANT:
            raise HTTPException(status_code=400, detail=f"Invalid assigned_consultant_id or user is not a consultant.")

    return crud.deliverable.create_deliverable(db=db, deliverable=deliverable)

@router.get("/project/{project_id}", response_model=List[schemas.Deliverable])
def read_deliverables_for_project(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Authorization: User should be PM of project, or consultant assigned to a deliverable in it, or Admin/FM
    # This is complex for a list view. For now, any active user can see deliverables if they know the project ID.
    # Finer-grained filtering could be applied in services layer or by modifying query.
    project = crud.project.get_project(db, project_id=project_id) # Check if project exists
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")

    deliverables = crud.deliverable.get_deliverables_by_project(db, project_id=project_id, skip=skip, limit=limit)
    return deliverables

@router.get("/{deliverable_id}", response_model=schemas.Deliverable)
def read_single_deliverable(deliverable_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_deliverable = crud.deliverable.get_deliverable(db, deliverable_id=deliverable_id)
    if db_deliverable is None:
        raise HTTPException(status_code=404, detail="Deliverable not found")
    # Authorization: PM of project, assigned consultant, Admin/FM
    # Similar to above, for now, any active user.
    return db_deliverable

@router.put("/{deliverable_id}", response_model=schemas.Deliverable)
def update_existing_deliverable(deliverable_id: int, deliverable_update_data: schemas.DeliverableUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_deliverable = crud.deliverable.get_deliverable(db, deliverable_id=deliverable_id)
    if db_deliverable is None:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    project = crud.project.get_project(db, project_id=db_deliverable.project_id) # Get associated project
    is_admin = current_user.role == models.user.UserRole.ADMIN
    is_pm_of_project = project and project.project_manager_id == current_user.id
    is_assigned_consultant = db_deliverable.assigned_consultant_id == current_user.id

    can_update = False
    if is_admin or (current_user.role == models.user.UserRole.PROJECT_MANAGER and is_pm_of_project):
        can_update = True # PMs/Admins can update most fields
    elif current_user.role == models.user.UserRole.CONSULTANT and is_assigned_consultant:
        # Consultants can only update specific fields (e.g., status, maybe effort spent if we add that)
        # For now, let's say they can update status.
        # Pydantic v1 uses .dict(), v2 uses .model_dump()
        update_fields_dict = deliverable_update_data.dict(exclude_unset=True)
        allowed_fields_for_consultant = {"status"}
        update_fields = {k for k, v in update_fields_dict.items() if v is not None}
        if update_fields.issubset(allowed_fields_for_consultant):
            can_update = True
        else:
            raise HTTPException(status_code=403, detail="Consultants can only update limited fields like status for their assigned deliverables.")

    if not can_update:
        raise HTTPException(status_code=403, detail="Not authorized to update this deliverable.")

    return crud.deliverable.update_deliverable(db=db, db_deliverable=db_deliverable, deliverable_in=deliverable_update_data)

@router.delete("/{deliverable_id}", response_model=schemas.Deliverable) # PMs or Admins can delete
def delete_single_deliverable(deliverable_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_project_manager_user)): # Ensures PM or Admin
    db_deliverable = crud.deliverable.get_deliverable(db, deliverable_id=deliverable_id)
    if db_deliverable is None:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    project = crud.project.get_project(db, project_id=db_deliverable.project_id)
    is_admin = current_user.role == models.user.UserRole.ADMIN
    is_pm_of_project = project and project.project_manager_id == current_user.id

    if not (is_admin or (current_user.role == models.user.UserRole.PROJECT_MANAGER and is_pm_of_project)):
        raise HTTPException(status_code=403, detail="Not authorized to delete this deliverable.")

    return crud.deliverable.delete_deliverable(db=db, db_deliverable=db_deliverable)
