from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ItemStatus(str, Enum):
    urgent = "Неотложная"
    non_urgent = "Несрочная"

class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[ItemStatus] = Field(default=ItemStatus.non_urgent)

class ItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: Optional[bool] = None
    status: Optional[ItemStatus] = None

class ItemOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    status: str
    created_at: str
