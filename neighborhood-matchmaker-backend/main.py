from fastapi import FastAPI
from routes import amenity, neighborhood, search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(amenity.router, prefix="/amenities")
app.include_router(neighborhood.router)
app.include_router(search.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}