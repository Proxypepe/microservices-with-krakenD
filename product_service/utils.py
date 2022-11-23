import uuid
import random

from schemas import Product

desc = ['awesome', 'good', 'not bad', 'bad', 'awful']


def generate_products(number) -> list[Product]:
    return [
        Product(
            id=i,
            name=str(uuid.uuid4()),
            description=random.choice(desc),
            price=random.randint(1000, 5000)
        ) for i in range(number)
    ]
