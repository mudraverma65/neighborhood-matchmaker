from enum import Enum as PyEnum
from fastapi import FastAPI

app = FastAPI()

class RentTypeEnum(PyEnum):
    STUDIO = "studio"
    ONE_BED = "One Bed"
    TWO_BED = "Two Bed"
    THREE_BED = "Three Bed"

@app.get("/rent-types", response_model=list[str])
async def get_rent_types():
    return [rent_type.value for rent_type in RentTypeEnum]
