from uuid import uuid4

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    token = Column(UUID(as_uuid=True), default=uuid4)

    posts = relationship("Post", back_populates="user")
