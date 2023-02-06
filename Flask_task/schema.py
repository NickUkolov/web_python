from pydantic import BaseModel, ValidationError

from errors import HttpError


class CreatePost(BaseModel):
    title: str
    description: str
    owner: str


def validate_create_post(json_data):
    try:
        post_schema = CreatePost(**json_data)
        return post_schema.dict()
    except ValidationError as e:
        raise HttpError(status_code=400, message=e.errors())
