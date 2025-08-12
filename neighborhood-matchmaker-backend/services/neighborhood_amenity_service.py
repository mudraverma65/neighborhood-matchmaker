from typing import List, Optional
from sqlalchemy.orm import Session
from dtos.neighborhood_search_dto import NeighborhoodSearchDTO
from dtos.search_result import NeighborhoodSearchResult, SearchResult
from services.amenity_service import AmenityService
from services.commute_service import CommuteService
from services.scoring_service import ScoringService
from services.database_service import DatabaseService
from enums.amenity_type import AmenityTypeEnum
import logging
import asyncio


class NeighborhoodAmenityService:
    """Service to handle neighborhood amenity processing"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.amenity_service = AmenityService(db_session)
        self.commute_service = CommuteService(db_session)
        self.scoring_service = ScoringService()
        self.database_service = DatabaseService(db_session)
    
    async def process_neighborhood_search(self, search_dto: NeighborhoodSearchDTO) -> SearchResult:
        """Process neighborhood search with clean architecture"""
        
        # If no amenities selected, use all available amenities
        amenities_to_search = search_dto.amenities or list(AmenityTypeEnum)
        
        # Get neighborhoods 
        neighborhoods = self.database_service.get_neighborhoods_with_coordinates(search_dto.city)
        
        if not neighborhoods:
            return self._create_empty_result(search_dto)
        
        # Process neighborhoods in batches for better performance
        results = await self._process_neighborhoods_batch(neighborhoods, search_dto, amenities_to_search)
        
        # Sort by score and limit results
        results.sort(key=lambda x: x.score, reverse=True)
        top_results = results[:10]
        
        return SearchResult(
            neighborhoods=top_results,
            total_results=len(top_results),
            search_criteria=search_dto.model_dump()
        )
    
    async def _process_neighborhoods_batch(
        self, 
        neighborhoods: List, 
        search_dto: NeighborhoodSearchDTO, 
        amenities_to_search: List[AmenityTypeEnum]
    ) -> List[NeighborhoodSearchResult]:
        """Process neighborhoods in batches"""
        
        results = []
        batch_size = 5  # Process 5 neighborhoods concurrently
        
        for i in range(0, len(neighborhoods), batch_size):
            batch = neighborhoods[i:i + batch_size]
            
            # Process batch concurrently
            batch_tasks = [
                self._process_single_neighborhood(neighborhood, search_dto, amenities_to_search)
                for neighborhood in batch
            ]
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            # Add successful results
            for result in batch_results:
                if not isinstance(result, Exception) and result is not None:
                    results.append(result)
            
            # Small delay between batches to be nice to external APIs
            if i + batch_size < len(neighborhoods):
                await asyncio.sleep(0.5)
        
        return results
    
    async def _process_single_neighborhood(
        self, 
        neighborhood, 
        search_dto: NeighborhoodSearchDTO,
        amenities_to_search: List[AmenityTypeEnum]
    ) -> Optional[NeighborhoodSearchResult]:
        """Process a single neighborhood"""
        
        try:
            # Get amenity counts
            amenity_counts = await self.amenity_service.get_amenity_counts(
                neighborhood, amenities_to_search
            )
            
            # Calculate commute time
            commute_time = self.commute_service.calculate_commute_time(
                neighborhood.coordinates.lat,
                neighborhood.coordinates.lon,
                search_dto.destination_neighborhood
            )
            
            # Calculate score
            score = self.scoring_service.calculate_neighborhood_score(
                amenity_counts=amenity_counts,
                requested_amenities=amenities_to_search,
                commute_time=commute_time,
                max_commute_time=search_dto.max_commute_time,
                is_preferred=(neighborhood.name in (search_dto.preferred_neighborhoods or [])),
                search_all_amenities=(not search_dto.amenities)  # Flag for dynamic scoring
            )
            
            return NeighborhoodSearchResult(
                neighborhood_id=neighborhood.id,
                neighborhood_name=neighborhood.name,
                amenity_counts=amenity_counts,
                total_amenities=sum(amenity_counts.values()),
                commute_time=commute_time or 0,
                score=score,
                coordinates={
                    "lat": neighborhood.coordinates.lat,
                    "lng": neighborhood.coordinates.lon
                }
            )
            
        except Exception as e:
            logging.error(f"Error processing neighborhood {neighborhood.name}: {e}")
            return None
    
    def _create_empty_result(self, search_dto: NeighborhoodSearchDTO) -> SearchResult:
        """Create empty result when no neighborhoods found"""
        return SearchResult(
            neighborhoods=[],
            total_results=0,
            search_criteria=search_dto.model_dump()
        )