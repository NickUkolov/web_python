import aiohttp.web
from aiohttp import web
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
import json

from db import Post, Base, User
from utils import hash_pw, check_pw

# TODO env for everything
# PG_DSN = 'postgresql+asyncpg://app:1234@db:5432/test_db'
PG_DSN = 'postgresql+asyncpg://app:1234@localhost:5431/test_db'

engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def orm_context(app: web.Application):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        return await handler(request)


@web.middleware
async def authentication_middleware(request: web.Request, handler):
    req_token = request.headers.get('token')
    if not req_token:
        raise web.HTTPForbidden(
            text=json.dumps({'status': 'error', 'message': 'enter the token'}),
            content_type='application/json',
        )

    session = request['session']
    db_query = select(User).where(User.token == req_token)
    try:
        db_res = await session.execute(db_query)
    except DBAPIError:
        raise web.HTTPForbidden(
            text=json.dumps({'status': 'error', 'message': 'enter correct length token'}),
            content_type='application/json',
        )
    user = db_res.scalar()
    request['token'] = [user.token, user.id]
    return await handler(request)


def check_owner(request, user_id):
    if not request['token'] or request['token'][1] != user_id:
        raise web.HTTPForbidden(
            text=json.dumps({'status': 'error', 'message': 'only owner has access'}),
            content_type='application/json',
        )
async def get_post(post_id: int, session: Session):
    post = await session.get(Post, post_id)

    if post is None:
        raise web.HTTPNotFound(
            text=json.dumps({'status': 'error', 'message': 'post not found'}),
            content_type='application/json',
        )

    return post


async def get_user(user_id: int, session: Session):
    user = await session.get(User, user_id)

    if user is None:
        raise web.HTTPNotFound(
            text=json.dumps({'status': 'error', 'message': 'user not found'}),
            content_type='application/json',
        )

    return user


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


class UserView(web.View):

    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        check_owner(self.request, user_id)
        session = self.request['session']
        user = await get_user(user_id, session)
        return web.json_response({
            'id': user.id,
            'name': user.name,
            'email': user.email,
        })

    async def post(self):
        session = self.request['session']
        user_data = await self.request.json()
        user_data['password'] = hash_pw(user_data['password'])
        user = User(**user_data)
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            raise web.HTTPConflict(
                text=json.dumps({'status': 'error', 'message': 'user already exists'}),
                content_type='application/json',
            )
        return web.json_response({'status': 'success', 'id': user.id})

    async def patch(self):
        session = self.request['session']
        user_id = int(self.request.match_info['user_id'])
        check_owner(self.request, user_id)
        user_data = await self.request.json()
        if 'password' in user_data:
            user_data['password'] = hash_pw(user_data['password'])
        user = await get_user(user_id, session)
        for key, value in user_data.items():
            setattr(user, key, value)
        session.add(user)
        await session.commit()
        return web.json_response({'status': 'patch success'})

    async def delete(self):
        session = self.request['session']
        user_id = int(self.request.match_info['user_id'])
        check_owner(self.request, user_id)
        user = await get_user(user_id, session)
        await session.delete(user)
        await session.commit()
        return web.json_response({'status': 'delete success'})


async def login(request):
    session = request['session']
    json_data = await request.json()
    db_query = select(User).where(User.name == json_data['name'])
    db_res = await session.execute(db_query)
    user = db_res.scalar()
    if not user or not check_pw(json_data['password'], user.password):
        raise web.HTTPUnauthorized(
            text=json.dumps({'status': 'error', 'message': 'incorrect login data'}),
            content_type='application/json',
        )
    return web.json_response({'token': str(user.token)})


async def main():
    app = web.Application()
    app.cleanup_ctx.append(orm_context)
    app.middlewares.append(session_middleware)
    app.middlewares.append(authentication_middleware)
    app.add_routes([
        web.get('/posts/{post_id:\d+}/', PostView),
        web.post('/posts/', PostView),
        web.delete('/posts/{post_id:\d+}/', PostView),
        web.patch('/posts/{post_id:\d+}/', PostView),

    ])
    app.add_routes([
        web.get('/users/{user_id:\d+}/', UserView),
        web.post('/users/', UserView),
        web.patch('/users/{user_id:\d+}/', UserView),
        web.delete('/users/{user_id:\d+}/', UserView),
        web.post('/login/', login)
    ])
    return app

app = main()
aiohttp.web.run_app(app, port=8081)