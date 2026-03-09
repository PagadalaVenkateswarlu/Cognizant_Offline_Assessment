from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    is_booked: bool = False
    user_id: int

class SlotCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    category_id: int
    week: int
    is_admin: bool
    # user_id: int


class BookSlot(BaseModel):
    user_id: Optional[int] = None
