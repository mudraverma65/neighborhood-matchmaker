from typing import Dict, List, Optional
from enums.amenity_type import AmenityTypeEnum


class ScoringService:
    """Service to handle neighborhood scoring with dynamic amenity weighting"""
    
    def __init__(self):
        # Base weights for different amenities
        self.amenity_weights = {
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
    
    def calculate_neighborhood_score(
        self, 
        amenity_counts: Dict[str, int], 
        requested_amenities: List[AmenityTypeEnum],
        commute_time: Optional[int], 
        max_commute_time: Optional[int] = None,
        is_preferred: bool = False,
        search_all_amenities: bool = False
    ) -> int:
        """
        Calculate neighborhood score with dynamic weighting
        
        Args:
            amenity_counts: Dictionary of amenity type -> count
            requested_amenities: List of amenities to consider
            commute_time: Commute time in minutes
            max_commute_time: Maximum acceptable commute time
            is_preferred: Whether this is a preferred neighborhood
            search_all_amenities: Whether user selected specific amenities or searching all
        """
        
        if search_all_amenities:
            # Dynamic scoring when no specific amenities selected
            amenity_score, max_amenity_score = self._calculate_dynamic_amenity_score(amenity_counts, requested_amenities)
        else:
            # Targeted scoring when user selected specific amenities
            amenity_score, max_amenity_score = self._calculate_targeted_amenity_score(amenity_counts, requested_amenities)
        
        # Calculate commute score
        commute_score, max_commute_score = self._calculate_commute_score(commute_time, max_commute_time)
        
        # Add preferred neighborhood bonus
        preferred_bonus = 5 if is_preferred else 0
        
        # Calculate final percentage score
        total_score = amenity_score + commute_score + preferred_bonus
        max_possible_score = max_amenity_score + max_commute_score + (5 if is_preferred else 0)
        
        if max_possible_score > 0:
            percentage_score = min(100, int((total_score / max_possible_score) * 100))
        else:
            percentage_score = 0
        
        return max(0, percentage_score)
    
    def _calculate_dynamic_amenity_score(self, amenity_counts: Dict[str, int], all_amenities: List[AmenityTypeEnum]) -> tuple[int, int]:
        """
        Dynamic scoring when user didn't select specific amenities
        Focuses on overall neighborhood livability
        """
        total_score = 0
        max_possible_score = 0
        
        # Calculate base amenity score
        for amenity_enum in all_amenities:
            amenity_key = amenity_enum.value
            count = amenity_counts.get(amenity_key, 0)
            weight = self.amenity_weights.get(amenity_enum, 5)
            
            # Dynamic scoring based on amenity availability
            amenity_score = self._get_dynamic_amenity_score(count, weight, amenity_enum)
            
            total_score += amenity_score
            max_possible_score += weight
        
        # Add diversity bonus - reward neighborhoods with variety of amenities
        diversity_bonus = self._calculate_diversity_bonus(amenity_counts)
        total_score += diversity_bonus
        max_possible_score += 10  # Max diversity bonus
        
        return total_score, max_possible_score
    
    def _calculate_targeted_amenity_score(self, amenity_counts: Dict[str, int], requested_amenities: List[AmenityTypeEnum]) -> tuple[int, int]:
        """
        Targeted scoring when user selected specific amenities
        Focuses on meeting specific needs
        """
        total_score = 0
        max_possible_score = 0
        
        for amenity_enum in requested_amenities:
            amenity_key = amenity_enum.value
            count = amenity_counts.get(amenity_key, 0)
            weight = self.amenity_weights.get(amenity_enum, 5)
            
            # Targeted scoring - more binary (have it or don't)
            amenity_score = self._get_targeted_amenity_score(count, weight)
            
            total_score += amenity_score
            max_possible_score += weight
        
        return total_score, max_possible_score
    
    def _get_dynamic_amenity_score(self, count: int, weight: int, amenity_type: AmenityTypeEnum) -> int:
        """
        Dynamic amenity scoring - considers both quantity and essential vs nice-to-have
        """
        # Essential amenities (grocery, transit, hospital) - higher threshold for full points
        essential_amenities = {AmenityTypeEnum.GROCERY, AmenityTypeEnum.TRANSIT, AmenityTypeEnum.HOSPITAL}
        
        if amenity_type in essential_amenities:
            if count >= 2:
                return weight  # Full points for 2+ essential amenities
            elif count == 1:
                return int(weight * 0.6)  # 60% for 1 essential amenity
            else:
                return 0  # No points for missing essential amenities
        else:
            # Nice-to-have amenities - more forgiving scoring
            if count >= 3:
                return weight
            elif count == 2:
                return int(weight * 0.8)
            elif count == 1:
                return int(weight * 0.5)
            else:
                return 0
    
    def _get_targeted_amenity_score(self, count: int, weight: int) -> int:
        """
        Targeted amenity scoring - user specifically wants this amenity
        """
        if count >= 3:
            return weight  # Full points for 3+ amenities
        elif count == 2:
            return int(weight * 0.8)  # 80% for 2 amenities
        elif count == 1:
            return int(weight * 0.5)  # 50% for 1 amenity
        else:
            return 0  # No points for missing requested amenities
    
    def _calculate_diversity_bonus(self, amenity_counts: Dict[str, int]) -> int:
        """
        Calculate bonus for amenity diversity - rewards well-rounded neighborhoods
        """
        # Count how many different types of amenities are available
        available_amenity_types = sum(1 for count in amenity_counts.values() if count > 0)
        total_amenity_types = len(AmenityTypeEnum)
        
        # Calculate diversity percentage
        diversity_percentage = available_amenity_types / total_amenity_types
        
        # Convert to bonus points (max 10 points)
        if diversity_percentage >= 0.8:
            return 10  # Excellent diversity
        elif diversity_percentage >= 0.6:
            return 7   # Good diversity
        elif diversity_percentage >= 0.4:
            return 4   # Fair diversity
        elif diversity_percentage >= 0.2:
            return 2   # Poor diversity
        else:
            return 0   # Very limited diversity
    
    def _calculate_commute_score(self, commute_time: Optional[int], max_commute_time: Optional[int]) -> tuple[int, int]:
        """Calculate commute-based score"""
        max_commute_points = 15  # Increased weight for commute
        
        if commute_time is None:
            return 0, 0
        
        if max_commute_time is not None:
            # User specified max commute preference
            if commute_time <= max_commute_time * 0.7:
                return max_commute_points, max_commute_points  # Excellent
            elif commute_time <= max_commute_time:
                return int(max_commute_points * 0.7), max_commute_points  # Good
            elif commute_time <= max_commute_time * 1.2:
                return int(max_commute_points * 0.3), max_commute_points  # Acceptable
            else:
                return 0, max_commute_points  # Unacceptable
        else:
            # General commute scoring
            if commute_time <= 15:
                return max_commute_points, max_commute_points
            elif commute_time <= 25:
                return int(max_commute_points * 0.8), max_commute_points
            elif commute_time <= 35:
                return int(max_commute_points * 0.6), max_commute_points
            elif commute_time <= 45:
                return int(max_commute_points * 0.3), max_commute_points
            else:
                return 0, max_commute_points