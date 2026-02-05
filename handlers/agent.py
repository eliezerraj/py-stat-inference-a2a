import logging
from opentelemetry import trace

from service.inference_stat import compute_stat

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

# Initialize Stat Service
def handler_compute_stat(payload: dict) -> dict:
    with tracer.start_as_current_span("handler.handler_compute_stat"):
        logger.info("def.handler_compute_stat()")  

        stat_data = compute_stat(payload["data"])

        return {
            "message": "stat computed",
            "data": stat_data
        }