from jaeger_client import Config, Tracer
from opentracing.scope_managers.contextvars import ContextVarsScopeManager
import logging


def init_tracer(service: str = 'product_service'):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
        scope_manager=ContextVarsScopeManager()
    )
    return config.initialize_tracer()



