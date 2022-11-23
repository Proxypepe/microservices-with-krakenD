import uuid
import random

from schemas import Category


def generate_categories(number) -> list[Category]:
    return [
        Category(
            id=i,
            name=str(uuid.uuid4()),
        ) for i in range(number)
    ]
