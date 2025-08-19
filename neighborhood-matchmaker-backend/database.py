import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from scripts.seed_neighborhoods import seed_neighborhoods_from_csv
from scripts.seed_neighborhood_rents import seed_neighborhood_rents

# DATABASE_URL for local or Render
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix legacy prefix if needed
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 👇 ensure tables are created on import
def init_db():
    from models import Neighborhood, Amenity  # import all models so Base knows them
    inspector = inspect(engine)
    print("Tables before create_all():", inspector.get_table_names())
    
    Base.metadata.create_all(bind=engine)
    print("Tables in metadata:", list(Base.metadata.tables.keys()))
    
    inspector = inspect(engine)
    print("Tables after create_all():", inspector.get_table_names())

    seed_neighborhoods_from_csv()
    seed_neighborhood_rents()

# run immediately when module loads
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
