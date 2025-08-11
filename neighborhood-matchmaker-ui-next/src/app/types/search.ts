import { AmenityTypeEnum, RentTypeEnum } from './enums';

export interface NeighborhoodSearchDTO {
  preferred_neighborhoods?: string[];
  budget: number;
  city: string;
  max_commute_time?: number;
  destination_neighborhood?: string;
  amenities?: AmenityTypeEnum[];
  rent_types?: RentTypeEnum[];
}

export interface NeighborhoodSearchResult {
  neighborhood_id: number;
  neighborhood_name: string;
  amenity_counts: Record<string, number>;
  total_amenities: number;
  commute_time?: number;
  score: number;
  coordinates: {
    lat: number;
    lng: number;
  };
}

export interface SearchResult {
  neighborhoods: NeighborhoodSearchResult[];
  total_results: number;
  search_criteria: Record<string, unknown>;
}
