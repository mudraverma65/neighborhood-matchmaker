from fastapi import FastAPI
from routes import amenity, neighborhood, search
from fastapi.middleware.cors import CORSMiddleware
from scripts.seed_neighborhoods import seed_neighborhoods_from_csv
from scripts.seed_neighborhood_rents import seed_neighborhood_rents
from contextlib import asynccontextmanager
from database import Base, engine
from sqlalchemy import inspect
import models

app = FastAPI()

app.include_router(amenity.router, prefix="/amenities")
app.include_router(neighborhood.router)
app.include_router(search.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("DB in use:", engine.url.render_as_string(hide_password=True))
    
    inspector = inspect(engine)
    print("Tables before create_all():", inspector.get_table_names())
    
    Base.metadata.create_all(bind=engine)
    print("Tables in metadata:", list(Base.metadata.tables.keys()))
    
    inspector = inspect(engine)
    print("Tables after create_all():", inspector.get_table_names())

    seed_neighborhoods_from_csv()
    seed_neighborhood_rents()

    yield

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