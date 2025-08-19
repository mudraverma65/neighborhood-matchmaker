import os
import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Neighborhood, NeighborhoodRent
from enums.rent_type import RentTypeEnum

CSV_PATH = os.path.join("data", "neighborhood_rents.csv")

def seed_neighborhood_rents():
    db: Session = SessionLocal()
    if db.query(Neighborhood).first():
        print("Neighborhoods already seeded, skipping...")
        db.close()
        return
    try:
        if not os.path.exists(CSV_PATH):
            raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")

        # Read CSV into DataFrame
        df = pd.read_csv(CSV_PATH)

        rents_by_neighborhood = {}

        for _, row in df.iterrows():
            neighborhood_name = row["neighborhood"]
            rent_type = RentTypeEnum(row["type"])
            avg_price = float(row["avg_price"])

            neighborhood = db.query(Neighborhood).filter_by(name=neighborhood_name).first()
            if not neighborhood:
                print(f"Neighborhood '{neighborhood_name}' not found, skipping...")
                continue

            rent_entry = NeighborhoodRent(
                neighborhood_id=neighborhood.id,
                type=rent_type,
                avg_price=avg_price
            )
            db.add(rent_entry)

            # Track for average price calculation
            rents_by_neighborhood.setdefault(neighborhood.id, []).append(avg_price)

        # Commit rents
        db.commit()

        # Update avg_price in Neighborhood
        for neighborhood_id, prices in rents_by_neighborhood.items():
            avg_price_calc = sum(prices) / len(prices)
            db.query(Neighborhood).filter_by(id=neighborhood_id).update(
                {Neighborhood.avg_price: avg_price_calc}
            )

        db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    seed_neighborhood_rents()
