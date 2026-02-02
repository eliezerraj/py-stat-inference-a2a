import logging
from opentelemetry import trace

from collections import defaultdict, deque
from datetime import timedelta

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class WindowStore:

    def __init__(self, window_size: int):
        self.data_store = defaultdict(lambda: deque(maxlen=window_size))

    def append(self, id: str, tps: int):
        with tracer.start_as_current_span("service.append"):
            logger.info("def.append()")

            self.data_store[id].append(tps)

            logger.debug("data_store: %s", self.data_store)
            
            return self.data_store
        
    def get(self, id: str):
        with tracer.start_as_current_span("service.get"):
            logger.info("def.get()")

            list_tps = list(self.data_store.get(id, []))

            logger.debug("list_tps: %s", list_tps)
            
            return list_tps       