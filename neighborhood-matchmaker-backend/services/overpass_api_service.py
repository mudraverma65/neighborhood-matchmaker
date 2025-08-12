import aiohttp
import asyncio
import logging
from typing import Dict, List, Optional
from enums.amenity_type import AmenityTypeEnum


class OverpassAPIService:
    """Clean Overpass API service without caching"""
    
    @classmethod
    async def get_amenity_counts(
        cls, 
        lat: float, 
        lon: float, 
        amenity_types: List[AmenityTypeEnum], 
        radius_meters: int = 1000
    ) -> Dict[str, int]:
        """Get amenity counts from Overpass API"""
        
        query = cls._build_overpass_query(lat, lon, amenity_types, radius_meters)
        
        try:
            # Add small delay to be respectful to the API
            await asyncio.sleep(1)
            
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    'https://overpass-api.de/api/interpreter',
                    data=query,
                    headers={'Content-Type': 'text/plain'}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return cls._parse_amenity_response(data, amenity_types)
                    
                    elif response.status == 429:  # Rate limited
                        logging.warning("Rate limited by Overpass API, waiting...")
                        await asyncio.sleep(30)
                        return await cls.get_amenity_counts(lat, lon, amenity_types, radius_meters)
                    
                    else:
                        logging.error(f"Overpass API error: {response.status}")
                        return {amenity.value: 0 for amenity in amenity_types}
                        
        except Exception as e:
            logging.error(f"Error querying Overpass API: {e}")
            return {amenity.value: 0 for amenity in amenity_types}
    
    @classmethod
    def _build_overpass_query(cls, lat: float, lon: float, amenity_types: List[AmenityTypeEnum], radius: int) -> str:
        """Build Overpass query for multiple amenities"""
        
        # Map amenity types to Overpass tags
        amenity_tags = {
            AmenityTypeEnum.GROCERY: ['shop=supermarket', 'shop=convenience', 'shop=grocery'],
            AmenityTypeEnum.RESTAURANT: ['amenity=restaurant', 'amenity=fast_food'],
            AmenityTypeEnum.CAFE: ['amenity=cafe', 'amenity=bar'],
            AmenityTypeEnum.HOSPITAL: ['amenity=hospital', 'amenity=clinic'],
            AmenityTypeEnum.SCHOOL: ['amenity=school', 'amenity=university'],
            AmenityTypeEnum.PARK: ['leisure=park', 'leisure=playground'],
            AmenityTypeEnum.TRANSIT: ['public_transport=station', 'railway=station'],
            AmenityTypeEnum.GYM: ['leisure=fitness_centre', 'leisure=sports_centre'],
            AmenityTypeEnum.LIBRARY: ['amenity=library']
        }
        
        # Build query parts
        query_parts = []
        
        for amenity_type in amenity_types:
            tags = amenity_tags.get(amenity_type, [f'amenity={amenity_type.value}'])
            
            for tag in tags:
                key, value = tag.split('=')
                query_parts.append(f'node["{key}"="{value}"](around:{radius},{lat},{lon});')
                query_parts.append(f'way["{key}"="{value}"](around:{radius},{lat},{lon});')
        
        # Combine into single query
        query = f"""
        [out:json][timeout:25];
        (
        {' '.join(query_parts)}
        );
        out center;
        """
        
        return query.strip()
    
    @classmethod
    def _parse_amenity_response(cls, data: Dict, amenity_types: List[AmenityTypeEnum]) -> Dict[str, int]:
        """Parse Overpass response and count amenities"""
        
        counts = {amenity.value: 0 for amenity in amenity_types}
        
        if 'elements' not in data:
            return counts
        
        # Count amenities by type
        for element in data['elements']:
            tags = element.get('tags', {})
            amenity_type = cls._classify_amenity(tags)
            
            if amenity_type and amenity_type in counts:
                counts[amenity_type] += 1
        
        return counts
    
    @classmethod
    def _classify_amenity(cls, tags: Dict[str, str]) -> Optional[str]:
        """Classify amenity based on its tags"""
        
        # Simple classification based on primary tags
        if 'shop' in tags:
            shop_type = tags['shop']
            if shop_type in ['supermarket', 'convenience', 'grocery']:
                return AmenityTypeEnum.GROCERY.value
            elif shop_type == 'bakery':
                return AmenityTypeEnum.CAFE.value
        
        if 'amenity' in tags:
            amenity_type = tags['amenity']
            if amenity_type in ['restaurant', 'fast_food']:
                return AmenityTypeEnum.RESTAURANT.value
            elif amenity_type in ['cafe', 'bar']:
                return AmenityTypeEnum.CAFE.value
            elif amenity_type in ['hospital', 'clinic']:
                return AmenityTypeEnum.HOSPITAL.value
            elif amenity_type in ['school', 'university']:
                return AmenityTypeEnum.SCHOOL.value
            elif amenity_type == 'library':
                return AmenityTypeEnum.LIBRARY.value
            elif amenity_type == 'gym':
                return AmenityTypeEnum.GYM.value
        
        if 'leisure' in tags:
            leisure_type = tags['leisure']
            if leisure_type in ['park', 'playground']:
                return AmenityTypeEnum.PARK.value
            elif leisure_type in ['fitness_centre', 'sports_centre']:
                return AmenityTypeEnum.GYM.value
        
        if 'public_transport' in tags or 'railway' in tags:
            return AmenityTypeEnum.TRANSIT.value
        
        return None