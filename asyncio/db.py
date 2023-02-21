from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


PG_DSN = 'postgresql+asyncpg://app:1234@127.0.0.1:5431/test_db'

engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class SwapiPeople(Base):

    __tablename__ = 'swapi_people'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


async def paste_to_db(item):
    swapi_person = SwapiPeople(
        id=item['id'],
        birth_year=item['birth_year'],
        eye_color=item['eye_color'],
        films=item['films'],
        gender=item['gender'],
        hair_color=item['hair_color'],
        height=item['height'],
        homeworld=item['homeworld'],
        mass=item['mass'],
        name=item['name'],
        skin_color=item['skin_color'],
        species=item['species'],
        starships=item['starships'],
        vehicles=item['vehicles'],
    )
    async with Session() as session:
        async with session.begin():
            session.add(swapi_person)
