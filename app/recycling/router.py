from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.recycling.schemas import RecyclingCreate, RecyclingResponse
from app.recycling import services

router = APIRouter(
    prefix="/recycling",
    tags=["Recycling"]
)


@router.post("/", response_model=RecyclingResponse, status_code=201)
def create_recycling(data: RecyclingCreate, db: Session = Depends(get_db)):
    return services.create_recycling_record(db, data)


@router.get("/user/{user_id}", response_model=list[RecyclingResponse])
def get_user_recycling(user_id: int, db: Session = Depends(get_db)):
    return services.get_recycling_by_user(db, user_id)


@router.get("/{recycling_id}", response_model=RecyclingResponse)
def get_recycling(recycling_id: int, db: Session = Depends(get_db)):
    recycling = services.get_recycling_by_id(db, recycling_id)
    if not recycling:
        raise HTTPException(status_code=404, detail="Recycling record not found")
    return recycling


@router.delete("/{recycling_id}", status_code=204)
def delete_recycling(recycling_id: int, db: Session = Depends(get_db)):
    recycling = services.get_recycling_by_id(db, recycling_id)
    if not recycling:
        raise HTTPException(status_code=404, detail="Recycling record not found")

    services.delete_recycling_record(db, recycling)
