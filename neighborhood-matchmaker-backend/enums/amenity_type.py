from enum import Enum as PyEnum
from fastapi import FastAPI

app = FastAPI()

class AmenityTypeEnum(PyEnum):
    PARK = "park"
    SCHOOL = "school"
    RESTAURANT = "restaurant"
    TRANSIT = "transit"
    GROCERY = "grocery"
    HOSPITAL = "hospital"
    CAFE = "cafe"
    LIBRARY = "library"
    GYM = "gym"

@app.get("/amenities", response_model=list[str])
async def get_amenities():
    return [amenity.value for amenity in AmenityTypeEnum]
