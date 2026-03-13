import logging
import numpy as np

from domain.model.entities import Stat

from opentelemetry import trace

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

#---------------------------------
# Compute Statistical Metrics
#---------------------------------
# Calculate slope of the time series data Linear regression to find the slope of the data points
def calc_slope(tps):
    x = np.arange(len(tps))
    slope, _ = np.polyfit(x, tps, 1)
    return slope

# window size
def calc_normalized_slope(tps):
    slope = calc_slope(tps)
    return slope / (np.mean(tps) + 1e-6)

def calc_fano_factor(tps):
    if tps.size < 2:
        return 0.0

    mean = np.mean(tps)
    if np.isclose(mean, 0.0):
        return 0.0

    variance = np.var(tps, ddof=1)
    return variance / (mean + 1e-6)


def calc_median_absolute_deviation(tps):
    median = np.median(tps)
    return float(np.median(np.abs(tps - median)))

def compute_stat(list_values: list[float]) -> Stat:
    with tracer.start_as_current_span("domain.service.inference_stat.compute_stat"):
        logger.info("def.compute_stat()")    
        logger.debug("values %s: ", list_values)

        if not list_values:
            logger.warning("No values enough provided for statistical computation.")
            return Stat()

        # Ensure we operate on a float numpy array
        tps_values = np.array(list_values, dtype=float)
        n = tps_values.size

        #Calculate mean
        mean = float(np.mean(tps_values))

        # Use sample variance when possible, otherwise 0.0 for single value
        if n > 1:
            variance = float(np.var(tps_values, ddof=1))
            stddev = float(np.sqrt(variance))
        else:
            variance = 0.0
            stddev = 0.0

        data_stat = Stat()

        data_stat.fano_factor = float(calc_fano_factor(tps_values))

        logger.debug(
            "computed distribution inputs mean=%s std=%s fano_factor=%s",
            mean,
            stddev,
            data_stat.fano_factor,
        )

        # Determine distribution type safely
        if mean > 0:
            if 0.9 < data_stat.fano_factor < 1.1:
                data_stat.distribution_type = "poisson"
            elif stddev < mean * 0.1:
                data_stat.distribution_type = "normal"
            elif stddev < mean * 0.5:
                data_stat.distribution_type = "uniform"
            else:
                data_stat.distribution_type = "exponential"
        else:
            data_stat.distribution_type = "constant"
        
        data_stat.mean = mean
        data_stat.std = stddev

        data_stat.range = float(np.max(tps_values) - np.min(tps_values))
        data_stat.p95 = float(np.percentile(tps_values, 95))
        data_stat.mad = calc_median_absolute_deviation(tps_values)

        # Normalized slope: guarded for small arrays and non-finite results
        if n > 1:
            try:
                n_slope = calc_normalized_slope(tps_values)
                n_slope = float(n_slope)
                if not np.isfinite(n_slope):
                    n_slope = 0.0
            except Exception:
                n_slope = 0.0
        else:
            n_slope = 0.0
        data_stat.n_slope = n_slope

        # Autocorrelation: guarded and coerced to finite float
        if n > 1:
            try:
                autocorr = float(np.corrcoef(tps_values[:-1], tps_values[1:])[0, 1])
            except Exception:
                autocorr = 0.0
            if not np.isfinite(autocorr):
                autocorr = 0.0
        else:
            autocorr = 0.0
        data_stat.autocorr = autocorr
    
        data_stat.min = float(np.min(tps_values))
        data_stat.max = float(np.max(tps_values))
        data_stat.sum = float(np.sum(tps_values))
        data_stat.population = float(n)
        
        return data_stat