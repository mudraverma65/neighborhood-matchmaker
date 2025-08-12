from dtos.neighborhood_search_dto import NeighborhoodSearchDTO 
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from dtos.amenity_count_result import AmenityCountResult
import asyncio
from services.overpass_api_service import OverpassAPIService
from models.neighborhood import Neighborhood
from models.coordinates import Coordinates
from models.amenity import Amenity
from enums.amenity_type import AmenityTypeEnum
import logging
from dtos.search_result import NeighborhoodSearchResult, SearchResult
from sqlalchemy import and_

class NeighborhoodAmenityService:
    """Service to handle neighborhood amenity processing"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    async def process_neighborhood_search(self, search_dto: NeighborhoodSearchDTO) -> SearchResult:
        
        if not search_dto.amenities:
            return self._get_all_amenities()
        
        neighborhoods = self._get_target_neighborhoods(search_dto)
        
        # if not neighborhoods:
        #     return []
        
        results = []
        for neighborhood in neighborhoods:
            try:
                if results: 
                    await asyncio.sleep(1)

                amenity_counts = await self.get_amenity_counts_with_cache(neighborhood, search_dto.amenities)

                commute_time = self._calculate_commute_time(
                    neighborhood.coordinates.lat,
                    neighborhood.coordinates.lon,
                    search_dto.destination_neighborhood
                )

                # Calculate neighborhood score
                score = self._calculate_neighborhood_score(
                    amenity_counts,
                    search_dto.amenities,
                    commute_time,
                    search_dto.max_commute_time,
                    is_preferred=(neighborhood.name in (search_dto.preferred_neighborhoods or []))
                )
                
                # Store amenity data in database
                await self._store_amenity_data(neighborhood.id, amenity_counts)

                result = NeighborhoodSearchResult(
                    neighborhood_id=neighborhood.id,
                    neighborhood_name=neighborhood.name,
                    amenity_counts=amenity_counts,
                    total_amenities=sum(amenity_counts.values()),
                    commute_time=commute_time or 0,
                    score=score,
                    coordinates={
                        "lat": neighborhood.coordinates.lat,
                        "lon": neighborhood.coordinates.lon
                    }
                )

                results.append(result)
                
                logging.info(f"Processed amenities for {neighborhood.name}")
                
            except Exception as e:
                logging.error(f"Error processing neighborhood {neighborhood.name}: {e}")
                continue

            results.sort(key=lambda x: x.score, reverse=True)

        top_results = results[:10]

        return SearchResult(
            neighborhoods=results,
            total_results=len(top_results),
            search_criteria=search_dto.model_dump()
        ).model_dump()
    
    def _get_target_neighborhoods(self, search_dto: NeighborhoodSearchDTO) -> List[Neighborhood]:
        """Get neighborhoods based on search criteria"""

        return self.db.query(Neighborhood).join(Coordinates).filter(
            Neighborhood.city == search_dto.city
        ).all()
    
    async def _store_amenity_data(self, neighborhood_id: int, amenity_counts: Dict[str, int]):
        """Store or update amenity data in the database"""
        
        try:
            for amenity_type_str, count in amenity_counts.items():
                # Convert string back to enum
                amenity_type_enum = AmenityTypeEnum(amenity_type_str)
                
                # Check if amenity record exists
                existing_amenity = self.db.query(Amenity).filter(
                    Amenity.type == amenity_type_enum,
                    Amenity.neighborhood_id == neighborhood_id
                ).first()
                
                if existing_amenity:
                    # Update existing record
                    existing_amenity.count = count
                else:
                    # Create new amenity record
                    new_amenity = Amenity(
                        type=amenity_type_enum,
                        count=count,
                        neighborhood_id=neighborhood_id
                    )
                    self.db.add(new_amenity)
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error storing amenity data: {e}")
            raise
    
    def _calculate_commute_time(self, origin_lat: float, origin_lon: float, destination_neighborhood_name: Optional[str]) -> Optional[int]:
        """Calculate estimated commute time between two neighborhoods (in minutes)"""
        
        if not destination_neighborhood_name:
            return None  # No destination specified
        
        import math
        
        # Get destination neighborhood coordinates
        destination_neighborhood = self.db.query(Neighborhood).join(Coordinates).filter(
            Neighborhood.name == destination_neighborhood_name
        ).first()
        
        if not destination_neighborhood:
            logging.warning(f"Destination neighborhood '{destination_neighborhood_name}' not found")
            return None
        
        dest_lat = destination_neighborhood.coordinates.lat
        dest_lon = destination_neighborhood.coordinates.lon
        
        # Haversine formula to calculate distance
        dest_lat_rad = math.radians(dest_lat)
        dest_lon_rad = math.radians(dest_lon)
        origin_lat_rad = math.radians(origin_lat)
        origin_lon_rad = math.radians(origin_lon)
        
        dlat = origin_lat_rad - dest_lat_rad
        dlon = origin_lon_rad - dest_lon_rad
        
        a = (math.sin(dlat/2)**2 + 
            math.cos(dest_lat_rad) * math.cos(origin_lat_rad) * 
            math.sin(dlon/2)**2)
        
        c = 2 * math.asin(math.sqrt(a))
        distance_km = 6371 * c  # Earth's radius in km
        
        # Average Montreal transit speed: ~20 km/h including stops/transfers
        commute_minutes = int((distance_km / 20) * 60) + 5
        
        return max(commute_minutes, 5)  # Minimum 5 minutes
    
    def _calculate_neighborhood_score(
        self, 
        amenity_counts: Dict[str, int], 
        requested_amenities: List[AmenityTypeEnum],
        commute_time: Optional[int], 
        max_commute_time: Optional[int] = None,
        is_preferred: bool = False  # NEW param
    ) -> int:
        """Calculate neighborhood score out of 100"""
        
        total_score = 0
        max_possible_score = 0

        AMENITY_WEIGHTS = {
            AmenityTypeEnum.GROCERY: 10,
            AmenityTypeEnum.TRANSIT: 9,
            AmenityTypeEnum.HOSPITAL: 9,
            AmenityTypeEnum.RESTAURANT: 8,
            AmenityTypeEnum.SCHOOL: 7,
            AmenityTypeEnum.PARK: 7,
            AmenityTypeEnum.CAFE: 6,
            AmenityTypeEnum.GYM: 6,
            AmenityTypeEnum.LIBRARY: 5,
        }

        for amenity_enum in requested_amenities:
            amenity_key = amenity_enum.value
            count = amenity_counts.get(amenity_key, 0)
            weight = AMENITY_WEIGHTS.get(amenity_enum, 5)
            
            if count >= 3:
                amenity_score = weight
            elif count == 2:
                amenity_score = int(weight * 0.8)
            elif count == 1:
                amenity_score = int(weight * 0.5)
            else:
                amenity_score = 0
            
            total_score += amenity_score
            max_possible_score += weight
        
        # Commute time scoring
        if commute_time is not None and max_commute_time is not None:
            if commute_time <= max_commute_time * 0.7:
                commute_bonus = 10
            elif commute_time <= max_commute_time:
                commute_bonus = 5
            elif commute_time <= max_commute_time * 1.2:
                commute_bonus = -5
            else:
                commute_bonus = -15
            
            total_score += commute_bonus
            max_possible_score += 10
        elif commute_time is not None:
            if commute_time <= 15:
                commute_bonus = 10
            elif commute_time <= 30:
                commute_bonus = 5
            elif commute_time <= 45:
                commute_bonus = 0
            else:
                commute_bonus = -10
            
            total_score += commute_bonus
            max_possible_score += 10
        
        # Add preferred neighborhood bonus points (fixed)
        if is_preferred:
            total_score += 5
            max_possible_score += 5

        # Convert to percentage (0-100)
        percentage_score = min(100, int((total_score / max_possible_score) * 100)) if max_possible_score > 0 else 0
        
        return max(0, percentage_score)

    async def get_amenity_counts_with_cache(self, neighborhood: Neighborhood, amenity_types: List[AmenityTypeEnum]) -> Dict[str, int]:
        existing_amenities = self.db.query(Amenity).filter(
            and_(
                Amenity.neighborhood_id == neighborhood.id,
                Amenity.type.in_(amenity_types)
            )
        ).all()

        existing_counts = {a.type: a.count for a in existing_amenities}

        if all(amenity in existing_counts for amenity in amenity_types):
            logging.info(f"Using cached amenity counts for neighborhood {neighborhood.name}")
            return {amenity.value: existing_counts.get(amenity, 0) for amenity in amenity_types}

        logging.info(f"Fetching amenity counts from Overpass for neighborhood {neighborhood.name}")
        fetched_counts = await OverpassAPIService.get_amenity_counts(
            neighborhood.coordinates.lat,
            neighborhood.coordinates.lon,
            amenity_types,
            radius_meters=1000
        )

        for amenity_enum in amenity_types:
            count = fetched_counts.get(amenity_enum.value, 0)
            existing_record = next((a for a in existing_amenities if a.type == amenity_enum), None)
            if existing_record:
                existing_record.count = count
            else:
                new_amenity = Amenity(type=amenity_enum, count=count, neighborhood_id=neighborhood.id)
                self.db.add(new_amenity)

        self.db.commit()
        return fetched_counts
    
    def _get_all_amenities(self) -> list[AmenityTypeEnum]:
        return [amenity for amenity in AmenityTypeEnum]
