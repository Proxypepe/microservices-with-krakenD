from fastapi import APIRouter, status, HTTPException, Depends
from schemas import Product, PostProduct
from mapper import mapping_model_schema
import models
import services

import logging
import opentracing
from jaeger_client import Tracer
from opentracing_instrumentation.request_context import get_current_span, span_in_context

router = APIRouter(
    tags=['Products'],
    prefix='/products',
)


@router.get(
    '/',
    status_code=200,
    response_model=list[Product],
)
async def get_all_products():
    tracer = opentracing.global_tracer()
    with tracer.start_span(get_all_products.__name__, child_of=get_current_span()) as span:
        with span_in_context(span):
            products = await services.get_all_products()
            l = len(products)
            span.set_tag('products_len', l)
            span.log_kv({'event': get_all_products.__name__, 'value': l})
            output = [
                mapping_model_schema(product)
                for product in products
            ]
            return output


# Don't work with '/', redirect error
@router.post(
    '/add',
    status_code=201,
    response_model=Product
)
async def add_new_product(product: PostProduct):
    tracer = opentracing.global_tracer()
    with tracer.start_span(__name__, child_of=get_current_span()) as span:
        with span_in_context(span):
            new_product = await services.create_product(product)
            new_product = Product(
                product_uuid=new_product.product_uuid,
                name=new_product.name,
                description=new_product.description,
                price=new_product.price,
            )
            return new_product


@router.delete('/{product_uuid}', status_code=status.HTTP_204_NO_CONTENT)
def add_new_product(product_uuid: str):
    raise HTTPException(
        status_code=404,
        detail=f"Not Found a product with id {product_uuid}",
    )
