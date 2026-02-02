import logging
from opentelemetry import trace

from config.config import settings

from service.window_store import WindowStore
from service.inference_stat import compute_stat

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

# Initialize Stat Service
data_store = WindowStore(settings.WINDOW_SIZE)

def handler_ingest(payload: dict) -> dict:
    with tracer.start_as_current_span("handler.ingest"):
        logger.info("def.handler_ingest()")  
        logger.debug("payload: %s", payload)

        tenant_id = payload["id"]
        tps = payload["tps"]
        
        window_data = data_store.append(tenant_id, tps)

        logger.debug("window_data %s:", window_data)

        if len(window_data.get(tenant_id)) < 3:
            return {
                "id": tenant_id,
                "window_size": len(window_data.get(tenant_id)),
                "message": "warming up"
            }
        
        data_stat = compute_stat(list(window_data.get(tenant_id)))

        return {
            "id": tenant_id,
            "window_size": len(window_data.get(tenant_id)),
            "message": "statistic computed",
            "stat": data_stat
        }
    
def handler_get_data(payload: dict) -> dict:
    with tracer.start_as_current_span("handler.handler_get_data"):
        logger.info("def.handler_get_data()")  
        logger.debug("payload: %s", payload)

        tenant_id = payload["id"]
        
        list_data = data_store.get(tenant_id)
        data_stat = compute_stat(list_data)

        return {
            "id": tenant_id,
            "message": "tenant tps list",
            "data": {   "stat":data_stat,
                        "tps":list_data,
                    }
        }