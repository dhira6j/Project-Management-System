from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, models
from ..database import get_db
from ..dependencies.auth import get_current_active_user, get_financial_manager_user, get_project_manager_user, get_admin_user # Added PM

router = APIRouter()

@router.post("/budgets/", response_model=schemas.ProjectBudgetInDB, dependencies=[Depends(get_financial_manager_user)])
def create_project_budget_entry(budget: schemas.ProjectBudgetCreate, db: Session = Depends(get_db)):
    proj = crud.project.get_project(db, project_id=budget.project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Project {budget.project_id} not found")
    existing_budget = crud.finance.get_project_budget(db, project_id=budget.project_id)
    if existing_budget:
        raise HTTPException(status_code=400, detail=f"Budget for project {budget.project_id} already exists.")
    return crud.finance.create_project_budget(db=db, budget=budget)

@router.get("/budgets/project/{project_id}", response_model=schemas.ProjectBudgetInDB)
def read_project_budget(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    budget = crud.finance.get_project_budget(db, project_id=project_id)
    if budget is None:
        raise HTTPException(status_code=404, detail=f"Budget for project {project_id} not found.")

    is_admin = current_user.role == models.user.UserRole.ADMIN
    is_fm = current_user.role == models.user.UserRole.FINANCIAL_MANAGER

    is_pm_of_project = False
    if current_user.role == models.user.UserRole.PROJECT_MANAGER:
        project = crud.project.get_project(db, project_id=project_id) # project itself is not budget.project
        if project and project.project_manager_id == current_user.id:
            is_pm_of_project = True

    if not (is_admin or is_fm or is_pm_of_project):
        raise HTTPException(status_code=403, detail="Not authorized to view this project budget.")
    return budget

@router.put("/budgets/project/{project_id}", response_model=schemas.ProjectBudgetInDB, dependencies=[Depends(get_financial_manager_user)])
def update_project_budget_entry(project_id: int, budget_update: schemas.ProjectBudgetUpdate, db: Session = Depends(get_db)):
    db_budget = crud.finance.get_project_budget(db, project_id=project_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail=f"Budget for project {project_id} not found to update.")
    return crud.finance.update_project_budget(db=db, db_budget=db_budget, budget_in=budget_update)

@router.post("/payments/", response_model=schemas.PaymentInDB, dependencies=[Depends(get_financial_manager_user)])
def create_new_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.finance.create_payment(db=db, payment=payment)

@router.get("/payments/project/{project_id}", response_model=List[schemas.PaymentInDB])
def read_payments_for_a_project(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    project = crud.project.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

    is_admin = current_user.role == models.user.UserRole.ADMIN
    is_fm = current_user.role == models.user.UserRole.FINANCIAL_MANAGER
    is_pm_of_project = (current_user.role == models.user.UserRole.PROJECT_MANAGER and project.project_manager_id == current_user.id)

    if not (is_admin or is_fm or is_pm_of_project):
        # Consultants might see their own payments later, but for now, this covers main roles.
        raise HTTPException(status_code=403, detail="Not authorized to view payments for this project.")

    payments = crud.finance.get_payments_for_project(db, project_id=project_id)
    return payments

@router.get("/payments/{payment_id}", response_model=schemas.PaymentInDB)
def read_single_payment(payment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)): # Changed dependency for inline check
    payment = crud.finance.get_payment(db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    # Authorization: FM, Admin, or PM of the project associated with the payment
    is_admin = current_user.role == models.user.UserRole.ADMIN
    is_fm = current_user.role == models.user.UserRole.FINANCIAL_MANAGER

    is_pm_of_project = False
    if current_user.role == models.user.UserRole.PROJECT_MANAGER:
        project = crud.project.get_project(db, project_id=payment.project_id)
        if project and project.project_manager_id == current_user.id:
            is_pm_of_project = True

    # Could also add check for consultant if payment.consultant_id == current_user.id

    if not (is_admin or is_fm or is_pm_of_project):
        raise HTTPException(status_code=403, detail="Not authorized to view this payment.")
    return payment

@router.put("/payments/{payment_id}", response_model=schemas.PaymentInDB, dependencies=[Depends(get_financial_manager_user)])
def update_existing_payment(payment_id: int, payment_update: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = crud.finance.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found to update")
    return crud.finance.update_payment(db=db, db_payment=db_payment, payment_in=payment_update)
