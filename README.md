# Neighborhood Matchmaker

Neighborhood Matchmaker is a web application that helps users find the best neighborhoods based on their lifestyle preferences. Users input criteria such as budget, commute time, preference for quiet or lively areas, and access to amenities. The app then returns the top neighborhoods that best match these preferences by pulling data from open APIs.

## Design Documentation

This project contains Mermaid scripts and generated diagrams related to the Neighborhood Matchmaker system.

### File Structure
- `design-docs/architecture/architecture-diagram.png` - High-level system architecture diagram
- `design-docs/er/er-diagram.png` - Entity Relationship (ER) diagram showing the database schema

### Data Sources
- **Montreal Neighborhood GeoJSON Data:** [donnees.montreal.ca](https://donnees.montreal.ca/)
- **Amenity Data:** Overpass API (OpenStreetMap)
- **Data Processing:** Claude.ai for CSV formatting

---

# Neighborhood Search System

## How It Works

### High-Level Flow
**User Request** → **Search** → **Process** → **Score** → **Return Results**

### Detailed Process

1. **User submits search criteria:**
   - City, destination neighborhood, max commute time
   - Optional: specific amenities, preferred neighborhoods

2. **NeighborhoodAmenityService processes the search:**
   - Retrieves all neighborhoods in the city from database
   - Processes neighborhoods in concurrent batches of 5 for optimal performance

3. **For each neighborhood (processed in parallel):**

   **a) Amenity Data Collection (AmenityService):**
   - Checks database for cached amenity counts
   - If data is missing → fetches from Overpass API
   - Stores new data in database for future searches

   **b) Commute Calculation (CommuteService):**
   - Looks up destination neighborhood coordinates
   - Calculates distance using Haversine formula
   - Estimates Montreal-specific transit time based on distance zones

   **c) Neighborhood Scoring (ScoringService):**
   - Applies intelligent scoring based on search type
   - Factors in commute time and user preferences
   - Returns 0-100 percentage score

4. **Results Compilation:**
   - Sorts neighborhoods by score (highest first)
   - Returns top 10 results with comprehensive data

---

## Scoring System

The system uses two distinct scoring approaches depending on user intent:

### Dynamic Scoring (All Amenities Search)
**Used when:** User doesn't specify particular amenities  
**Goal:** Find the most livable, well-rounded neighborhoods

**Key Features:**
- **Essential vs Nice-to-Have Classification:**
  ```
  Essential (stricter scoring): Grocery, Transit, Hospital
  Nice-to-Have (more forgiving): Restaurants, Cafes, Gyms, etc.
  ```

- **Tiered Scoring:**
  - Essential amenities: Need 2+ for full points, 1 = 60% points
  - Nice-to-have amenities: 3+ = full points, scaling down to 1 = 50% points

- **Diversity Bonus (up to 10 points):**
  - 80%+ amenity types available = +10 points
  - 60-80% = +7 points  
  - 40-60% = +4 points
  - Prevents gaming (e.g., 20 restaurants but no grocery stores)

### Targeted Scoring (Specific Amenities Search)
**Used when:** User selects specific amenities  
**Goal:** Does this neighborhood meet my specific needs?

**Key Features:**
- **Binary Focus:** Either you have what I want or you don't
- **Simplified Scoring:**
  - 3+ amenities = full points
  - 2 amenities = 80% points
  - 1 amenity = 50% points
  - 0 amenities = 0 points
- **No diversity bonus** - focused on user's explicit requirements

### Amenity Weights (Montreal-Optimized)
```
Grocery: 10     # Most important for daily life
Transit: 9      # Critical in Montreal
Hospital: 9     # Safety/emergency access
Restaurant: 8   # Social/convenience
School: 7       # Important for families
Park: 7         # Quality of life
Cafe: 6         # Nice to have
Gym: 6          # Lifestyle
Library: 5      # Least critical
```

### Commute Scoring
- **User-specified max commute:** Scores based on preference thresholds
- **General commute bands:**
  - ≤15 minutes: Excellent (full points)
  - 16-25 minutes: Good (80% points)
  - 26-35 minutes: Fair (60% points)
  - 36-45 minutes: Poor (30% points)
  - 45+ minutes: Unacceptable (0 points)

### Additional Factors
- **Preferred Neighborhood Bonus:** +5 points for user-specified preferred areas
- **Montreal-Specific Transit Modeling:** Realistic speed estimates based on distance zones

---

## Performance Optimizations

- **Concurrent Processing:** 5 neighborhoods processed simultaneously
- **Smart Caching:** Database stores API results to minimize external calls
- **Batch Processing:** Small delays between batches to respect API limits
- **Graceful Error Handling:** Failed neighborhoods are skipped, processing continues

---

## Example Scenarios

### Scenario A: General Search (Dynamic Scoring)
- **Neighborhood:** 1 grocery, 0 transit, 5 restaurants, 2 cafes
- **Result:** Lower score despite many restaurants (missing essential transit)
- **Reasoning:** System prioritizes livability over abundance in one category

### Scenario B: Specific Search for "Restaurants + Cafes" (Targeted Scoring)
- **Same neighborhood:** 5 restaurants, 2 cafes  
- **Result:** High score
- **Reasoning:** Excellent match for user's specific requirements