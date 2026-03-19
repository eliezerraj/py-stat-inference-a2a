import logging

from pydantic import ValidationError

from domain.model.entities import StatRequest
from domain.service.inference_stat import compute_stat
from shared.exception.exceptions import A2ARequestError

from opentelemetry import trace
#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

def _validate_payload(payload: dict) -> StatRequest:
    try:
        if hasattr(StatRequest, "model_validate"):
            request = StatRequest.model_validate(payload)
        else:
            request = StatRequest.parse_obj(payload)
        return request.ensure_finite()
    except (ValidationError, TypeError, ValueError) as exc:
        raise A2ARequestError(
            "Payload must include a non-empty 'data' array with finite numeric values."
        ) from exc

# Initialize Stat Service
def handler_compute_stat(payload: dict) -> dict:
    with tracer.start_as_current_span("infrastructure.adapter.handler_compute_stat") as span:
        logger.info("def.handler_compute_stat()")  

        stat_request = _validate_payload(payload)
        stat_data = compute_stat(stat_request.data)

        return {
            "message": "stat computed",
            "data": stat_data
        }