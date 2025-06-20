from sqlalchemy.orm import Session
from .. import models, schemas

def get_deliverable(db: Session, deliverable_id: int):
    return db.query(models.Deliverable).filter(models.Deliverable.id == deliverable_id).first()

def get_deliverables_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Deliverable).filter(models.Deliverable.project_id == project_id).offset(skip).limit(limit).all()

def create_deliverable(db: Session, deliverable: schemas.DeliverableCreate):
    db_deliverable = models.Deliverable(**deliverable.dict()) # Use model_dump for Pydantic v2
    db.add(db_deliverable)
    db.commit()
    db.refresh(db_deliverable)
    return db_deliverable

def update_deliverable(db: Session, db_deliverable: models.Deliverable, deliverable_in: schemas.DeliverableUpdate):
    data = deliverable_in.dict(exclude_unset=True) # Use model_dump for Pydantic v2
    for key, value in data.items():
        setattr(db_deliverable, key, value)
    db.add(db_deliverable)
    db.commit()
    db.refresh(db_deliverable)
    return db_deliverable

def delete_deliverable(db: Session, db_deliverable: models.Deliverable):
    db.delete(db_deliverable)
    db.commit()
    return db_deliverable
