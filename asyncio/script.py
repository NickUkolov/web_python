import asyncio
from datetime import datetime

from aiohttp import ClientSession
from more_itertools import chunked

from db import *


async def count_people(session):
    async with session.get('https://swapi.dev/api/people/') as response:
        num = await response.json()
        return num['count']


async def get_person(id, session):
    async with session.get('https://swapi.dev/api/people/' + f'{id}') as response:
        data = await response.json()
        data['id'] = id
        if response.status == 200:
            return data
        else:
            return None


async def get_coroutines(number, session):
    async with session as session:
        for chunk in chunked(range(1, number + 1), 10):
            coroutines = [get_person(str(i), session) for i in chunk]
            yield await asyncio.gather(*coroutines)


async def dict_create(persons, session):
    person_dict = {}
    for person in persons:
        if person is None:
            continue
        person.pop('created', None)
        person.pop('edited', None)
        person.pop('url', None)
        person['homeworld'] = await change_fields(person['homeworld'], session=session)
        person['vehicles'] = ', '.join([await change_fields(url, session) for url in person['vehicles']])
        person['species'] = ', '.join([await change_fields(url, session) for url in person['species']])
        person['starships'] = ', '.join([await change_fields(url, session) for url in person['starships']])
        person['films'] = ', '.join([await change_fields(url, session) for url in person['films']])

        person_dict[person['id']] = person
    return person_dict


async def change_fields(url, session):
    async with session.get(url) as response:
        response = await response.json()
        if 'title' in response:
            return response['title']
        if 'name' in response:
            return response['name']
        return None


async def insert_person(person_dict):
    async with Session() as session:
        for val in person_dict.values():
            await paste_to_db(val)
        await session.commit()


async def main():
    session = ClientSession()
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)
        await con.commit()

    number = await asyncio.wait_for(count_people(session), timeout=None)
    tasks = []
    async for person in get_coroutines(number, session=session):
        task_1 = asyncio.create_task(dict_create(person, session=session))
        tasks.append(task_1)
        task_2 = asyncio.create_task(insert_person(await task_1))
        tasks.append(task_2)

    await asyncio.gather(*tasks)
    await session.close()

if __name__ == '__main__':
    start = datetime.now()
    asyncio.run(main())
    end = datetime.now()
    print(f'Успешно за {end - start}, смотрите бд!=)')
