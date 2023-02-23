from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
