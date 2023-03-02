from pydantic import BaseModel, ValidationError

from models import HttpError


class CreatePost(BaseModel):
    title: str
    description: str
    owner_id: str


def validate(json_data):
    try:
        post_schema = CreatePost(**json_data)
        return post_schema.dict()
    except ValidationError as e:
        raise HttpError(status_code=400, message=e.errors())
