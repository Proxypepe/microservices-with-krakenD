import schemas
import models
from jaeger_client import Tracer
from opentracing_instrumentation.request_context import get_current_span, span_in_context
import opentracing
import deps


@deps.trace_it(tag='mapper', value='model to schema')
def mapping_model_schema(model: models.Product):
    schema = schemas.Product(
        product_uuid=model.product_uuid,
        name=model.name,
        description=model.description,
        price=model.price,
    )
    return schema


@deps.trace_it(tag='mapper', value='schema to model')
def mapping_schema_model(schema: schemas.Product):
    model = schemas.Product(
        product_uuid=schema.product_uuid,
        name=schema.name,
        description=schema.description,
        price=schema.price,
    )
    return model

