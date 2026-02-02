import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import StatusCode, Status 

from exception.exceptions import A2ARouterError
from a2a import envelope
from handlers.ingest import handler_ingest, handler_get_data

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

#---------------------------------
# A2A Router
class A2ARouter:
    
    def route(self, envelope):
        with tracer.start_as_current_span("a2a.route") as span:
            logger.info("def.route()")  

            try:
                if envelope.message_type == "STAT_TPS":
                    return handler_ingest(envelope.payload)
                elif envelope.message_type == "LIST_TPS":
                    return handler_get_data(envelope.payload)
                else:
                    message = f"Unsupported message type: {envelope.message_type}"
                    e = A2ARouterError(message)
                    raise e
                           
            except A2ARouterError as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                logger.error("Error clustering data", exc_info=e)
                raise e

            except Exception as e:
                logger.error("Error clustering data", exc_info=e)
                raise e
