from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import amenity
from database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(amenity.router, prefix="/amenities")

@app.get("/")
async def root():
    return {"message": "Hello World"}