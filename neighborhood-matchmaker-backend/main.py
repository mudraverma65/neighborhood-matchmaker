from fastapi import FastAPI
from routes import amenity
app = FastAPI()

app.include_router(amenity.router, prefix="/amenities")

@app.get("/")
async def root():
    return {"message": "Hello World"}