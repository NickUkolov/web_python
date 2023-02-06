import atexit

from sqlalchemy import Column, String, Integer, DateTime, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_dsn = 'postgresql://app:1234@127.0.0.1:5431/netology'
engine = create_engine(db_dsn)
Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


Base.metadata.create_all(bind=engine)
