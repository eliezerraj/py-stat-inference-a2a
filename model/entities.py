from pydantic import BaseModel
from typing import Optional

class Tenant(BaseModel):
    id: str
    tps: int
    timestamp: Optional[str] = None
    message: Optional[str] = None
    window_size: Optional[int] = None
    stat: Optional['Stat'] = None

class Stat(BaseModel):
    distribution_type: Optional[str] = None
    confidence: Optional[float] = None
    std: Optional[float] = None
    mean: Optional[float] = None
    variance: Optional[float] = None
    max: Optional[float] = None
    min: Optional[float] = None
    population: Optional[float] = None