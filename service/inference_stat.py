import logging
from opentelemetry import trace

from model.entities import Stat

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

#---------------------------------
# Compute Statistical Metrics

def compute_stat(values: list, confidence: float = 0.95) -> dict:
    with tracer.start_as_current_span("service.compute_stat"):
        logger.info("def.compute_stat()")    
        logger.debug("def.compute_stat()", extra={"values": values})

        if not values:
            logger.warning("No values provided for statistical computation.")
            return Stat()   
        
        mean = sum(values) / len(values)

        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        stddev = variance ** 0.5

        data_stat = Stat()

        if stddev < mean * 0.1:
            data_stat.distribution_type = "normal"
        elif stddev < mean * 0.5:
            data_stat.distribution_type = "uniform"
        else:
            data_stat.distribution_type = "exponential"

        data_stat.mean = mean
        data_stat.variance = variance
        data_stat.std = stddev
        data_stat.confidence = confidence
        data_stat.max = max(values)
        data_stat.min = min(values)
        data_stat.population = sum(values)

        return data_stat