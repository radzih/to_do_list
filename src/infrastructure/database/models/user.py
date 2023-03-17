from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.infrastructure.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user")
