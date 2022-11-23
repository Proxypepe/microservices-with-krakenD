from fastapi import APIRouter, status, HTTPException
from schemas import Category, PostCategory
from utils import generate_categories


router = APIRouter(
    tags=['Category'],
    prefix='/categories',
)

serial = 5
categories = generate_categories(serial)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[Category])
async def get_all_categories():
    return categories


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Category)
async def add_new_product(product: PostCategory):
    global serial
    new_category = Category(
        id=serial,
        name=product.name,
    )
    serial += 1
    categories.append(new_category)
    return new_category


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def add_new_product(category_id: int):
    for i, category in enumerate(categories):
        if category.id == category_id:
            categories.pop(i)
            return
    raise HTTPException(
        status_code=404,
        detail=f"Not Found a category with id {category_id}",
    )
