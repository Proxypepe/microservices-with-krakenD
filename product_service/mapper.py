import schemas
import models
from jaeger_client import Tracer
from opentracing_instrumentation.request_context import get_current_span, span_in_context
import opentracing


def mapping_model_schema(model: models.Product):
    tracer = opentracing.global_tracer()
    with tracer.start_span(mapping_model_schema.__name__, child_of=get_current_span()) as span:
        with span_in_context(span):
            try:
                schema = schemas.Product(
                    product_uuid=model.product_uuid,
                    name=model.name,
                    description=model.description,
                    price=model.price,
                )
                span.set_tag('event', 'Mapping')
                span.log_kv({'event': mapping_model_schema.__name__, 'value': True})
                return schema
            except Exception as e:
                span.set_tag('error', e.__name__)
                span.log_kv({'event': mapping_model_schema.__name__, 'value': e.__name__})


def mapping_schema_model(schema: schemas.Product):
    tracer = opentracing.global_tracer()
    with tracer.start_span(mapping_schema_model.__name__, child_of=get_current_span()) as span:
        with span_in_context(span):
            try:
                model = schemas.Product(
                    product_uuid=schema.product_uuid,
                    name=schema.name,
                    description=schema.description,
                    price=schema.price,
                )
                span.set_tag('event', 'Mapping')
                span.log_kv({'event': mapping_schema_model.__name__, 'value': True})
                return model
            finally:
                span.set_tag('error', True)
                span.log_kv({'event': mapping_schema_model.__name__, 'value': False})
                return None

