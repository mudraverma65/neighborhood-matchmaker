import logging
from enums.amenity_type import AmenityTypeEnum
from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import requests
import asyncio
import aiohttp
from urllib.parse import quote
import logging

class OverpassAPIService:
    """Service to fetch amenity counts from OpenStreetMap via Overpass API"""
    
    OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    
    @classmethod
    def _amenity_enum_to_osm_tag(cls, amenity_enum: AmenityTypeEnum) -> str:
        """Convert AmenityTypeEnum to OpenStreetMap amenity tag"""
        # Map your enum values to OSM amenity tags
        mapping = {
            AmenityTypeEnum.PARK: "park",
            AmenityTypeEnum.SCHOOL: "school",
            AmenityTypeEnum.RESTAURANT: "restaurant",
            AmenityTypeEnum.TRANSIT: "public_transport",  # OSM uses different tag
            AmenityTypeEnum.GROCERY: "supermarket",      # Map grocery to supermarket
            AmenityTypeEnum.HOSPITAL: "hospital",
            AmenityTypeEnum.CAFE: "cafe",
            AmenityTypeEnum.LIBRARY: "library",
            AmenityTypeEnum.GYM: "fitness_centre",       # OSM uses fitness_centre
        }
        return mapping.get(amenity_enum, amenity_enum.value)
    
    @classmethod
    async def get_amenity_counts(cls, latitude: float, longitude: float, 
                               amenity_types: List[AmenityTypeEnum], 
                               radius_meters: int = 1000) -> Dict[str, int]:
        """Fetch amenity counts around coordinates"""
        
        # Separate transit from other amenities since it uses different OSM tags
        regular_amenities = [a for a in amenity_types if a != AmenityTypeEnum.TRANSIT]
        has_transit = AmenityTypeEnum.TRANSIT in amenity_types
        
        # Convert enum values to OSM tags for regular amenities
        osm_tags = [cls._amenity_enum_to_osm_tag(amenity) for amenity in regular_amenities]
        
        # Build query parts
        query_parts = []
        
        # Regular amenities query
        if osm_tags:
            amenity_filter = '|'.join(osm_tags)
            query_parts.append(f'node["amenity"~"{amenity_filter}"](around:{radius_meters},{latitude},{longitude});')
            query_parts.append(f'way["amenity"~"{amenity_filter}"](around:{radius_meters},{latitude},{longitude});')
            query_parts.append(f'relation["amenity"~"{amenity_filter}"](around:{radius_meters},{latitude},{longitude});')
        
        # Transit query (uses public_transport tag)
        if has_transit:
            query_parts.append(f'node["public_transport"~"platform|station|stop_position"](around:{radius_meters},{latitude},{longitude});')
            query_parts.append(f'way["public_transport"~"platform|station"](around:{radius_meters},{latitude},{longitude});')
            query_parts.append(f'relation["public_transport"~"platform|station"](around:{radius_meters},{latitude},{longitude});')
        
        query = f"""
        [out:json][timeout:25];
        (
          {chr(10).join(query_parts)}
        );
        out;
        """
        
        try:
            # Create SSL context that skips certificate verification
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(
                    cls.OVERPASS_URL,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'},
                    data=f'data={quote(query)}'
                ) as response:
                    data = await response.json()
                    
                    # Initialize counts
                    counts = {cls._amenity_enum_to_osm_tag(amenity): 0 for amenity in regular_amenities}
                    if has_transit:
                        counts['public_transport'] = 0
                    
                    # Count elements
                    for element in data.get('elements', []):
                        tags = element.get('tags', {})
                        
                        # Check for regular amenities
                        amenity_type = tags.get('amenity')
                        if amenity_type and amenity_type in counts:
                            counts[amenity_type] += 1
                        
                        # Check for transit
                        if has_transit and tags.get('public_transport'):
                            counts['public_transport'] += 1
                    
                    # Convert back to enum string representation for storage
                    enum_counts = {}
                    for amenity_enum in amenity_types:
                        if amenity_enum == AmenityTypeEnum.TRANSIT:
                            enum_counts[amenity_enum.value] = counts.get('public_transport', 0)
                        else:
                            osm_tag = cls._amenity_enum_to_osm_tag(amenity_enum)
                            enum_counts[amenity_enum.value] = counts.get(osm_tag, 0)
                    
                    return enum_counts
                    
        except Exception as e:
            logging.error(f"Error fetching amenity data: {e}")
            return {amenity.value: 0 for amenity in amenity_types}
