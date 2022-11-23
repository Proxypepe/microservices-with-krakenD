from fastapi import APIRouter, status, HTTPException
from schemas import Product, PostProduct
from utils import generate_products


router = APIRouter(
    tags=['Products'],
    prefix='/products',
)

serial = 5
products = generate_products(serial)


@router.get('/', status_code=200, response_model=list[Product])
async def get_all_products():
    return products


# Don't work with '/', redirect error
@router.post('/add', status_code=201, response_model=Product)
async def add_new_product(product: PostProduct):
    global serial
    new_product = Product(
        id=serial,
        name=product.name,
        description=product.description,
        price=product.price,
    )
    serial += 1
    products.append(new_product)
    return new_product


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def add_new_product(product_id: int):
    for i, product in enumerate(products):
        if product.id == product_id:
            products.pop(i)
            return
    raise HTTPException(
        status_code=404,
        detail=f"Not Found a product with id {product_id}",
    )
