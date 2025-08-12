from typing import List
from sqlalchemy.orm import Session, joinedload
from models.neighborhood import Neighborhood
from models.coordinates import Coordinates
import logging


class DatabaseService:
    """Clean database operations service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def get_neighborhoods_with_coordinates(self, city: str) -> List[Neighborhood]:
        """Get neighborhoods with coordinates using optimized query"""
        try:
            # Use joinedload to prevent N+1 query problem
            neighborhoods = self.db.query(Neighborhood).options(
                joinedload(Neighborhood.coordinates)
            ).join(Coordinates).filter(
                Neighborhood.city == city
            ).all()
            
            logging.info(f"Retrieved {len(neighborhoods)} neighborhoods for city: {city}")
            return neighborhoods
            
        except Exception as e:
            logging.error(f"Error fetching neighborhoods for city {city}: {e}")
            return []
    
    def get_neighborhood_by_name(self, name: str, city: str = None) -> Neighborhood:
        """Get single neighborhood by name"""
        try:
            query = self.db.query(Neighborhood).options(
                joinedload(Neighborhood.coordinates)
            ).filter(Neighborhood.name == name)
            
            if city:
                query = query.filter(Neighborhood.city == city)
            
            return query.first()
            
        except Exception as e:
            logging.error(f"Error fetching neighborhood {name}: {e}")
            return None