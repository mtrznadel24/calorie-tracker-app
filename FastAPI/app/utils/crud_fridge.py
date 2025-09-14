from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.exceptions import NotFoundError
from app.models import Fridge
from app.utils.crud import get_or_404


def get_fridge_object_or_404(db: Session, model, fridge_id: int, object_id: int):
    obj = db.query(model).filter(
        model.id == object_id,
        model.fridge_id == fridge_id
    ).first()
    if not obj:
        raise NotFoundError(f"{model.__name__} does not exist")
    return obj

def create_fridge_instance(db: Session, model, fridge_id: int, data: dict):
    fridge_in = get_or_404(db, Fridge, fridge_id) # If fridge does not exist, it will raise an exception
    obj = model(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_fridge_object(db: Session, model, fridge_id: int, object_id: int, data: BaseModel):
    obj = get_fridge_object_or_404(db, model, fridge_id, object_id)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj

def delete_fridge_object(db: Session, model, fridge_id: int, object_id: int):
    obj = get_fridge_object_or_404(db, model, fridge_id, object_id)
    db.delete(obj)
    db.commit()
    return obj