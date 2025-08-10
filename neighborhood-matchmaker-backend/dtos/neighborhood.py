from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from enums.amenity_type import AmenityTypeEnum
from enums.rent_type import RentTypeEnum

class NeighborhoodSearchDTO(BaseModel):
    preferred_neighborhoods: Optional[List[int]]  # IDs or names
    budget: int
    city: str
    max_commute_time: Optional[int]
    amenities: Optional[List[AmenityTypeEnum]]
    rent_types: Optional[List[RentTypeEnum]]
