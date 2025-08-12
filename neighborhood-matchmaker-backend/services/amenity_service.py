from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.amenity import Amenity
from enums.amenity_type import AmenityTypeEnum
from services.overpass_api_service import OverpassAPIService
import logging


class AmenityService:
    """Service to handle amenity-related operations"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
    async def get_amenity_counts(self, neighborhood, amenity_types: List[AmenityTypeEnum]) -> Dict[str, int]:
        """Get amenity counts - check database first, then fetch from API if needed"""
        
        # Check what we have in database
        existing_amenities = self._get_stored_amenities(neighborhood.id, amenity_types)
        existing_counts = {a.type: a.count for a in existing_amenities}
        
        # Identify missing amenities
        missing_amenities = [amenity for amenity in amenity_types if amenity not in existing_counts]
        
        # If we have all amenities stored, return them
        if not missing_amenities:
            logging.info(f"Using stored amenity data for neighborhood {neighborhood.name}")
            return {amenity.value: existing_counts.get(amenity, 0) for amenity in amenity_types}
        
        # Fetch missing amenities from external API
        logging.info(f"Fetching {len(missing_amenities)} missing amenities for {neighborhood.name}")
        
        try:
            fetched_counts = await OverpassAPIService.get_amenity_counts(
                neighborhood.coordinates.lat,
                neighborhood.coordinates.lon,
                missing_amenities,
                radius_meters=1000
            )
            
            # Store the newly fetched amenity data
            self._store_amenity_data(neighborhood.id, fetched_counts, missing_amenities)
            
            # Combine existing and fetched data
            final_counts = {}
            for amenity_enum in amenity_types:
                if amenity_enum in existing_counts:
                    final_counts[amenity_enum.value] = existing_counts[amenity_enum]
                else:
                    final_counts[amenity_enum.value] = fetched_counts.get(amenity_enum.value, 0)
            
            return final_counts
            
        except Exception as e:
            logging.error(f"Error fetching amenities for {neighborhood.name}: {e}")
            # Return what we have in database, zeros for missing
            return {amenity.value: existing_counts.get(amenity, 0) for amenity in amenity_types}
    
    def _get_stored_amenities(self, neighborhood_id: int, amenity_types: List[AmenityTypeEnum]) -> List[Amenity]:
        """Get amenities stored in database"""
        return self.db.query(Amenity).filter(
            and_(
                Amenity.neighborhood_id == neighborhood_id,
                Amenity.type.in_(amenity_types)
            )
        ).all()
    
    def _store_amenity_data(self, neighborhood_id: int, amenity_counts: Dict[str, int], amenity_types: List[AmenityTypeEnum]):
        """Store amenity data in database"""
        try:
            for amenity_enum in amenity_types:
                count = amenity_counts.get(amenity_enum.value, 0)
                
                # Check if record already exists
                existing_record = self.db.query(Amenity).filter(
                    and_(
                        Amenity.type == amenity_enum,
                        Amenity.neighborhood_id == neighborhood_id
                    )
                ).first()
                
                if existing_record:
                    # Update existing record
                    existing_record.count = count
                else:
                    # Create new record
                    new_amenity = Amenity(
                        type=amenity_enum,
                        count=count,
                        neighborhood_id=neighborhood_id
                    )
                    self.db.add(new_amenity)
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error storing amenity data: {e}")
            raise