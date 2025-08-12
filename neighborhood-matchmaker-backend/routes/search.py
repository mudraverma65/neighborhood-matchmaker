from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from dtos.neighborhood_search_dto import NeighborhoodSearchDTO
from dtos.amenity_count_result import AmenityCountResult
from database import get_db
from typing import List
from services.neighborhood_amenity_service import NeighborhoodAmenityService
import logging
from dtos.search_result import SearchResult

router = APIRouter()

@router.post("/search-neighborhoods", response_model=SearchResult)
async def search_neighborhoods(
    search_dto: NeighborhoodSearchDTO,
    db: Session = Depends(get_db)
):
    """Endpoint to search neighborhoods and fetch amenity data"""
    
    try:
        service = NeighborhoodAmenityService(db)
        results = await service.process_neighborhood_search(search_dto)
        
        if not results:
            raise HTTPException(status_code=404, detail="No neighborhoods found matching criteria")
        
        return results
        
    except Exception as e:
        logging.error(f"Error in neighborhood search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
