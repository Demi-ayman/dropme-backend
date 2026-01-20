from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.recycling.models import Recycling
from app.recycling.schemas import RecyclingCreate
from app.users.models import User
from app.common.exceptions import BusinessRuleException
from app.core.config import settings


POINTS_PER_KG = {
    "plastic": 10,
    "glass": 8,
    "metal": 15,
    "paper": 5,
}


def calculate_points(material_type: str, weight: float) -> int:
    rate = POINTS_PER_KG.get(material_type.lower())
    if rate is None:
        raise BusinessRuleException(
            message="Unsupported material type"
        )
    return int(weight * rate)


def check_daily_limit(db: Session, user_id: int):
    today_start = datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    count_today = (
        db.query(Recycling)
        .filter(
            Recycling.user_id == user_id,
            Recycling.created_at >= today_start
        )
        .count()
    )

    if count_today >= settings.MAX_RECYCLES_PER_DAY:
        raise BusinessRuleException(
            message="Daily recycling limit exceeded"
        )


def check_duplicate_recycling(
    db: Session,
    user_id: int,
    material_type: str,
    weight_kg: float
):
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

    duplicate = (
        db.query(Recycling)
        .filter(
            Recycling.user_id == user_id,
            Recycling.material_type == material_type,
            Recycling.weight_kg == weight_kg,
            Recycling.created_at >= five_minutes_ago
        )
        .first()
    )

    if duplicate:
        raise BusinessRuleException(
            message="Duplicate recycling detected"
        )


def create_recycling_record(db: Session, data: RecyclingCreate) -> Recycling:
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise BusinessRuleException(
            message="User not found"
        )

    check_daily_limit(db, user.id)
    check_duplicate_recycling(
        db,
        user.id,
        data.material_type,
        data.weight_kg
    )

    points = calculate_points(
        data.material_type,
        data.weight_kg
    )

    recycling = Recycling(
        user_id=user.id,
        material_type=data.material_type,
        weight_kg=data.weight_kg,
        points_earned=points,
    )

    user.points += points

    db.add(recycling)
    db.commit()
    db.refresh(recycling)

    return recycling


def get_recycling_by_user(db: Session, user_id: int):
    return (
        db.query(Recycling)
        .filter(Recycling.user_id == user_id)
        .all()
    )


def get_recycling_by_id(db: Session, recycling_id: int):
    return (
        db.query(Recycling)
        .filter(Recycling.id == recycling_id)
        .first()
    )


def delete_recycling_record(db: Session, recycling: Recycling):
    raise BusinessRuleException(
        message="Deleting recycling records is not allowed"
    )
  