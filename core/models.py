from app.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
