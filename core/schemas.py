from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BlogBase(BaseModel):
    title: str
    description: str


class BlogCreate(BlogBase):
    pass


class BlogRead(BlogBase):
    id: int
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True
