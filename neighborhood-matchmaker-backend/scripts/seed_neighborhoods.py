import pandas as pd
import os
from database import SessionLocal
from models import Neighborhood, Coordinates

CSV_PATH = os.path.join("data", "neighborhood_coordinates.csv")

def seed_neighborhoods_from_csv():
    df = pd.read_csv(CSV_PATH)

    db = SessionLocal()

    if db.query(Neighborhood).first():
        print("Neighborhoods already seeded, skipping...")
        db.close()
        return
    
    try:
        for _, row in df.iterrows():
            # Create coordinates entry
            coord = Coordinates(lat=row["latitude"], lon=row["longitude"])
            db.add(coord)
            db.flush() 

            # Create neighborhood entry
            neighborhood = Neighborhood(
                name=row["neighborhood"],
                city="Montreal",
                coordinates_id=coord.id
            )
            db.add(neighborhood)

        db.commit()
        print("✅ Neighborhoods seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding neighborhoods: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_neighborhoods_from_csv()
