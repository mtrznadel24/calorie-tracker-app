from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.exceptions import NotFoundError


def get_or_404(db: Session, model, object_id: int):
    obj = db.query(model).filter(model.id == object_id).first()
    if not obj:
        raise NotFoundError(f"{model.__name__} with id {id} not found")
    return obj

def create_instance(db: Session, model, data: dict):
    obj = model(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_by_id(db: Session, model, object_id: int, data: BaseModel):
    obj = get_or_404(db, model, object_id)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj

def delete_by_id(db: Session, model, object_id: int):
    obj = get_or_404(db, model, object_id)
    db.delete(obj)
    db.commit()
    return obj