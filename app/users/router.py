from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.users import models, schemas
from app.common.responses import success_response
from app.common.exceptions import BusinessRuleException

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user_in.email)
        .first()
    )
    if existing_user:
        raise BusinessRuleException(
            message="Email already registered",
            status_code=status.HTTP_409_CONFLICT
        )

    new_user = models.User(email=user_in.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return success_response(
        data=schemas.UserResponse.model_validate(new_user),
        message="User registered successfully"
    )

@router.get(
    "/{user_id}",
    response_model=dict
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return success_response(
        data=schemas.UserResponse.model_validate(user)
    )
