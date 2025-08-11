from fastapi import FastAPI
from routes import amenity, neighborhood, search

app = FastAPI()

app.include_router(amenity.router, prefix="/amenities")
app.include_router(neighborhood.router)
app.include_router(search.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}