import {
  NeighborhoodSearchDTO,
  SearchResult,
} from "../types/search";

export type Amenity = string;
export type Neighborhood = string;

// Backend base URL
const BASE_URL = "http://localhost:8000";

export async function fetchAmenities(): Promise<Amenity[]> {
  const res = await fetch(`${BASE_URL}/amenities`);
  if (!res.ok) throw new Error("Failed to fetch amenities");
  const data: Amenity[] = await res.json();
  return data;
}

export async function fetchNeighborhoods(): Promise<Neighborhood[]> {
  const res = await fetch(`${BASE_URL}/neighborhoods`);
  if (!res.ok) throw new Error("Failed to fetch neighborhoods");
  const data: Neighborhood[] = await res.json();
  return data;
}

export async function searchNeighborhoods(
  searchDto: NeighborhoodSearchDTO
): Promise<SearchResult> {
  const res = await fetch(`${BASE_URL}/search-neighborhoods`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(searchDto),
  });

  if (!res.ok) {
    throw new Error("Failed to search neighborhoods");
  }

  const data: SearchResult = await res.json();
  return data;
}
