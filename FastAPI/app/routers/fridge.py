from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, services
from typing import List

router = APIRouter(prefix="/fridge", tags=["fridge"])

@router.post("/products", response_model=schemas.FridgeProductRead)
def add_fridge_product(item_in: schemas.FridgeProductCreate, db: Session = Depends(get_db)):
    return services.create_fridge_product(item_in, db)

@router.get("/products", response_model=List[schemas.FridgeProductRead])
def read_fridge_products(db: Session = Depends(get_db)):
    return services.get_fridge_products(db)

@router.get("/products/{product_id}", response_model=schemas.FridgeProductRead)
def read_fridge_product(product_id: int, db: Session = Depends(get_db)):
    result = services.get_fridge_product(product_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Fridge product not found")
    return result