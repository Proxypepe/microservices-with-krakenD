from pydantic import BaseModel
import uuid


class PostProduct(BaseModel):
    name: str
    description: str
    price: int


class Product(PostProduct):
    product_uuid: uuid.UUID

    class Config:
        orm_mode = True

