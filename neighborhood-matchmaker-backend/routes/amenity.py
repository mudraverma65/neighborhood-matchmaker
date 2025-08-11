from fastapi import APIRouter
from enum import Enum
from enums.amenity_type import AmenityTypeEnum

router = APIRouter()

@router.get("/", response_model=list[str])
async def get_amenities():
    return [amenity.value for amenity in AmenityTypeEnum]
