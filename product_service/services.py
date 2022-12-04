from models import Product
import schemas
import uuid
from jaeger_client import Tracer
from opentracing_instrumentation.request_context import get_current_span, span_in_context
import opentracing


async def get_all_products() -> list[Product]:
    tracer = opentracing.global_tracer()
    with tracer.start_span(get_all_products.__name__, child_of=get_current_span()) as span:
        with span_in_context(span):
            return Product.objects


async def create_product(product: schemas.PostProduct) -> Product:
    prod = Product(
        product_uuid=uuid.uuid4(),
        name=product.name,
        description=product.description,
        price=product.price,
    ).save()
    return prod
