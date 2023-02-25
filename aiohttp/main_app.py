import json
from typing import Type, Callable, Awaitable

from aiohttp import web
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from db import Post, Base, User
from utils import hash_pw, check_pw

# TODO env for everything
PG_DSN = 'postgresql+asyncpg://app:1234@db:5432/test_db'

engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

ERROR_TYPE = (
    Type[web.HTTPUnauthorized]
    | Type[web.HTTPForbidden]
    | Type[web.HTTPNotFound]
    | Type[web.HTTPBadRequest]
    | Type[web.HTTPConflict]
)


def raise_http_error(error_type: ERROR_TYPE, message: str | dict):
    raise error_type(
        text=json.dumps({"status": "error", "message": message}),
        content_type="application/json",
    )


async def orm_context(app: web.Application):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@web.middleware
async def session_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    async with Session() as session:
        request["session"] = session
        return await handler(request)


@web.middleware
async def authentication_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    req_token = request.headers.get("token")
    if not req_token:
        raise_http_error(web.HTTPForbidden, "enter the token")

    session = request["session"]
    db_query = select(User).where(User.token == req_token)
    try:
        db_res = await session.execute(db_query)
    except DBAPIError:
        raise web.HTTPForbidden(
            text=json.dumps(
                {"status": "error", "message": "enter correct length token"}
            ),
            content_type="application/json",
        )
    user = db_res.scalar()
    if user is None:
        raise_http_error(web.HTTPNotFound, "user not found")
    request["token"] = [user.token, user.id]
    return await handler(request)


def check_owner(request: web.Request, user_id: int) -> None:
    if not request["token"] or request["token"][1] != user_id:
        raise_http_error(web.HTTPForbidden, "only the owner has access")


async def get_db_item(
    item_id: int, model_name: Type[User] | Type[Post], session: Session
) -> User | Post:
    item = await session.get(model_name, item_id)
    if item is None:
        raise_http_error(web.HTTPNotFound, f"{model_name.__name__} not found")
    return item


class PostView(web.View):
    async def get(self):
        session = self.request["session"]
        post_id = int(self.request.match_info["post_id"])
        post = await get_db_item(item_id=post_id, model_name=Post, session=session)
        return web.json_response(
            {
                "title": post.title,
                "description": post.description,
                "owner": post.owner,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
            }
        )

    async def post(self):
        session = self.request["session"]
        data = await self.request.json()
        user_id = self.request["token"][1]
        data["user_id"] = user_id
        user = await get_db_item(item_id=user_id, model_name=User, session=session)
        if data["owner"] != user.name:
            raise_http_error(
                web.HTTPBadRequest, "you can use only your user name as owner in post"
            )

        post = Post(**data)
        session.add(post)
        # try:
        await session.commit()
        # except IntegrityError:
        #     raise web.HTTPConflict(
        #         text=json.dumps({'status': 'error', 'message': 'user already exists'}),
        #         content_type='application/json',
        #     )

        return web.json_response({"status": "success", "post_id": post.id})

    async def patch(self):
        session = self.request["session"]
        post_id = int(self.request.match_info["post_id"])
        post = await get_db_item(item_id=post_id, model_name=Post, session=session)

        check_owner(self.request, post.user_id)

        data = await self.request.json()

        if any(key in data.keys() for key in ("created_at", "owner", "user_id")):
            raise_http_error(
                web.HTTPBadRequest, "you can change only title or description"
            )

        for key, value in data.items():
            setattr(post, key, value)
        session.add(post)
        await session.commit()

        return web.json_response({"status": "patch success"})

    async def delete(self):
        session = self.request["session"]
        post_id = int(self.request.match_info["post_id"])
        post = await get_db_item(item_id=post_id, model_name=Post, session=session)

        check_owner(self.request, post.user_id)

        await session.delete(post)
        await session.commit()
        return web.json_response({"status": "delete success"})


class UserView(web.View):
    async def get(self):
        user_id = int(self.request.match_info["user_id"])
        check_owner(self.request, user_id)
        session = self.request["session"]
        user = await get_db_item(item_id=user_id, model_name=User, session=session)
        return web.json_response(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            }
        )

    async def post(self):
        session = self.request["session"]
        user_data = await self.request.json()
        user_data["password"] = hash_pw(user_data["password"])
        user = User(**user_data)
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            raise_http_error(web.HTTPConflict, "user already exists")

        return web.json_response({"status": "success", "id": user.id})

    async def patch(self):
        session = self.request["session"]
        user_id = int(self.request.match_info["user_id"])
        check_owner(self.request, user_id)
        user_data = await self.request.json()
        if "password" in user_data:
            user_data["password"] = hash_pw(user_data["password"])
        user = await get_db_item(item_id=user_id, model_name=User, session=session)
        for key, value in user_data.items():
            setattr(user, key, value)
        session.add(user)
        await session.commit()
        return web.json_response({"status": "patch success"})

    async def delete(self):
        session = self.request["session"]
        user_id = int(self.request.match_info["user_id"])
        check_owner(self.request, user_id)
        user = await get_db_item(item_id=user_id, model_name=User, session=session)
        await session.delete(user)
        await session.commit()
        return web.json_response({"status": "delete success"})


async def login(request: web.Request) -> web.Response:
    session = request["session"]
    json_data = await request.json()
    db_query = select(User).where(User.name == json_data["name"])
    db_res = await session.execute(db_query)
    user = db_res.scalar()
    if not user or not check_pw(json_data["password"], user.password):
        raise_http_error(web.HTTPUnauthorized, "incorrect login or password")

    return web.json_response({"token": str(user.token)})


async def main() -> web.Application:
    app = web.Application(middlewares=[session_middleware])
    auth_app = web.Application(
        middlewares=[session_middleware, authentication_middleware]
    )
    app.cleanup_ctx.append(orm_context)
    app.add_routes(
        [
            web.post("/api/register/", UserView),
            web.post("/api/login/", login),
            web.get("/api/posts/{post_id:\d+}/", PostView),
        ]
    )

    auth_app.add_routes(
        [
            web.post("/posts/", PostView),
            web.delete("/posts/{post_id:\d+}/", PostView),
            web.patch("/posts/{post_id:\d+}/", PostView),
            web.get("/users/{user_id:\d+}/", UserView),
            web.patch("/users/{user_id:\d+}/", UserView),
            web.delete("/users/{user_id:\d+}/", UserView),
        ]
    )

    app.add_subapp(prefix="/api", subapp=auth_app)

    return app
