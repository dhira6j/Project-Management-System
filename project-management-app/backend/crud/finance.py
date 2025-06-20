from sqlalchemy.orm import Session
from .. import models, schemas

# ProjectBudget CRUD
def get_project_budget(db: Session, project_id: int):
    return db.query(models.ProjectBudget).filter(models.ProjectBudget.project_id == project_id).first()

def create_project_budget(db: Session, budget: schemas.ProjectBudgetCreate):
    db_budget = models.ProjectBudget(**budget.dict()) # Use model_dump for Pydantic v2
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def update_project_budget(db: Session, db_budget: models.ProjectBudget, budget_in: schemas.ProjectBudgetUpdate):
    data = budget_in.dict(exclude_unset=True) # Use model_dump for Pydantic v2
    for key, value in data.items():
        setattr(db_budget, key, value)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

# Payment CRUD
def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()

def get_payments_for_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Payment).filter(models.Payment.project_id == project_id).offset(skip).limit(limit).all()

def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(**payment.dict()) # Use model_dump for Pydantic v2
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment(db: Session, db_payment: models.Payment, payment_in: schemas.PaymentUpdate):
    data = payment_in.dict(exclude_unset=True) # Use model_dump for Pydantic v2
    for key, value in data.items():
        setattr(db_payment, key, value)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment
