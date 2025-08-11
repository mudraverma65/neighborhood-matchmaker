from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class NeighborhoodSearchResult(BaseModel):
    neighborhood_id: int
    neighborhood_name: str
    amenity_counts: Dict[str, int]
    total_amenities: int
    commute_time: Optional[int]
    score: int
    coordinates: Dict[str, float]

class SearchResult(BaseModel):
    neighborhoods: List[NeighborhoodSearchResult]
    total_results: int
    search_criteria: Dict[str, Any]