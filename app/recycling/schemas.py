from pydantic import BaseModel,Field
from typing import Literal
from datetime import datetime

class RecyclingCreate(BaseModel):
    user_id: int
    material_type: Literal["plastic","glass", "metal", "paper"]
    weight_kg: float=Field(gt=0)


class RecyclingResponse(BaseModel):
    id: int
    user_id: int
    material_type: str
    weight_kg: float
    points_earned: int
    created_at: datetime

    class Config:
        from_attributes = True
