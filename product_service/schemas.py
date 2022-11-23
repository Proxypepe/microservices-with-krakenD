from pydantic import BaseModel


class PostProduct(BaseModel):
    name: str
    description: str
    price: int


class Product(PostProduct):
    id: int


