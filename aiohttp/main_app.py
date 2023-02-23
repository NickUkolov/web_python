from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import json

from db import Post, Base

PG_DSN = 'postgresql+asyncpg://app:1234@db:5432/test_db'

engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def orm_context(app: web.Application):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@web.middleware
async def session_middleware(requests: web.Request, handler):
    async with Session() as session:
        requests['session'] = session
        return await handler(requests)


async def get_post(post_id: int, session: Session):
    post = await session.get(Post, post_id)

    if post is None:
        raise web.HTTPNotFound(
            text=json.dumps({'status': 'error', 'message': 'post not found'}),
            content_type='application/json',
        )

    return post


class PostView(web.View):

    async def get(self):
        session = self.request['session']
        post_id = int(self.request.match_info['post_id'])
        post = await get_post(post_id, session)
        return web.json_response({
            'title': post.title,
            'description': post.description,
            'owner': post.owner,
            'created_at': post.created_at.isoformat()
        })

    async def post(self):
        session = self.request['session']
        data = await self.request.json()
        post = Post(**data)
        session.add(post)
        try:
            await session.commit()
        except IntegrityError:
            raise web.HTTPConflict(
                text=json.dumps({'status': 'error', 'message': 'user already exists'}),
                content_type='application/json',
            )

        return web.json_response({'status': 'success', 'post_id': post.id})

    async def patch(self):
        session = self.request['session']
        post_id = int(self.request.match_info['post_id'])
        post = await get_post(post_id, session)
        data = await self.request.json()
        for key, value in data.items():
            setattr(post, key, value)
        session.add(post)
        await session.commit()

        return web.json_response({'status': 'patch success'})

    async def delete(self):
        session = self.request['session']
        post_id = int(self.request.match_info['post_id'])
        post = await get_post(post_id, session)
        await session.delete(post)
        await session.commit()
        return web.json_response({'status': 'delete success'})


async def main():
    app = web.Application()
    app.cleanup_ctx.append(orm_context)
    app.middlewares.append(session_middleware)
    app.add_routes([
        web.get('/posts/{post_id:\d+}/', PostView),
        web.post('/posts/', PostView),
        web.delete('/posts/{post_id:\d+}/', PostView),
        web.patch('/posts/{post_id:\d+}/', PostView),

    ])
    return app
