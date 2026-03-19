import math
from typing import Optional

from pydantic import BaseModel, Field

class StatRequest(BaseModel):
    data: list[float] = Field(min_length=1)

    def ensure_finite(self) -> "StatRequest":
        if any(not math.isfinite(value) for value in self.data):
            raise ValueError("data must contain only finite numeric values")
        return self

class Stat(BaseModel):
    distribution_type: Optional[str] = None
    mean: Optional[float] = None
    std: Optional[float] = None

    range: Optional[float] = None
    p95: Optional[float] = None
    median_abs_deviation: Optional[float] = None
    n_slope: Optional[float] = None
    autocorr: Optional[float] = None
    fano_factor: Optional[float] = None

    min: Optional[float] = None
    max: Optional[float] = None
    sum: Optional[float] = None
    population: Optional[float] = None