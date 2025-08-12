from typing import Optional, Tuple
from sqlalchemy.orm import Session
from models.neighborhood import Neighborhood
from models.coordinates import Coordinates
import math
import logging


class CommuteService:
    """Service to handle commute time calculations"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def calculate_commute_time(self, origin_lat: float, origin_lon: float, destination_neighborhood_name: Optional[str]) -> Optional[int]:
        """Calculate estimated commute time between origin and destination"""
        
        if not destination_neighborhood_name:
            return None
        
        # Get destination coordinates
        dest_coords = self._get_destination_coordinates(destination_neighborhood_name)
        if not dest_coords:
            return None
        
        dest_lat, dest_lon = dest_coords
        
        # Calculate distance and convert to commute time
        distance_km = self._calculate_distance_km(origin_lat, origin_lon, dest_lat, dest_lon)
        return self._estimate_transit_time(distance_km)
    
    def _get_destination_coordinates(self, destination_name: str) -> Optional[Tuple[float, float]]:
        """Get coordinates for destination neighborhood"""
        try:
            destination = self.db.query(Neighborhood).join(Coordinates).filter(
                Neighborhood.name == destination_name
            ).first()
            
            if not destination:
                logging.warning(f"Destination neighborhood '{destination_name}' not found")
                return None
            
            return (destination.coordinates.lat, destination.coordinates.lon)
            
        except Exception as e:
            logging.error(f"Error fetching destination coordinates: {e}")
            return None
    
    def _calculate_distance_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        
        # Convert to radians
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(dlon/2)**2)
        
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c  # Earth's radius in km
    
    def _estimate_transit_time(self, distance_km: float) -> int:
        """Estimate transit time based on Montreal transportation patterns"""
        
        # Montreal transit speed patterns based on distance
        if distance_km <= 2:
            # Walking distance or very short transit
            avg_speed_kmh = 15
            base_waiting_time = 5
        elif distance_km <= 5:
            # Local bus/short metro
            avg_speed_kmh = 18
            base_waiting_time = 8
        elif distance_km <= 10:
            # Metro or express bus
            avg_speed_kmh = 25
            base_waiting_time = 10
        else:
            # Long distance with potential transfers
            avg_speed_kmh = 22
            base_waiting_time = 15
        
        # Calculate travel time + waiting/transfer time
        travel_time = int((distance_km / avg_speed_kmh) * 60)
        total_time = travel_time + base_waiting_time
        
        return max(total_time, 5)  # Minimum 5 minutes