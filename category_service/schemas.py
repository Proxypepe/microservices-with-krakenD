from pydantic import BaseModel


class PostCategory(BaseModel):
    name: str


class Category(PostCategory):
    id: int


