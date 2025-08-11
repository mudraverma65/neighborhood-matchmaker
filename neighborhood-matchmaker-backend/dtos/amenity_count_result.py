from pydantic import BaseModel
from typing import Dict

class AmenityCountResult(BaseModel):
    neighborhood_id: int
    neighborhood_name: str
    amenity_counts: Dict[str, int]
    total_amenities: int
    commute_time: int
    scpre: int