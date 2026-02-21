/**
 * Service to load and search parishes from local JSON file
 */

export interface Parish {
  id: number;
  name: string;
  diocese: string;
  address: string;
  city: string;
  state: string;
  zip: string;
  country: string;
  phone?: string;
  website?: string;
  email?: string;
  latitude: number;
  longitude: number;
}

let parishesCache: Parish[] | null = null;

/**
 * Load all parishes from JSON file
 */
async function loadParishes(): Promise<Parish[]> {
  if (parishesCache) {
    return parishesCache;
  }

  try {
    const response = await fetch('/parishes.json');
    if (!response.ok) {
      throw new Error('Failed to load parishes');
    }
    parishesCache = await response.json();
    return parishesCache!;
  } catch (error) {
    console.error('Error loading parishes:', error);
    throw error;
  }
}

/**
 * Calculate distance between two coordinates using Haversine formula
 */
function haversineDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const R = 3959; // Earth radius in miles
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

/**
 * Search for parishes near coordinates
 */
export async function searchParishes(
  latitude: number,
  longitude: number,
  radiusMiles: number = 50
): Promise<(Parish & { distance: number })[]> {
  try {
    const allParishes = await loadParishes();

    // Filter by distance and add distance property
    const results = allParishes
      .map((parish) => {
        if (!parish.latitude || !parish.longitude) {
          return null;
        }
        const distance = haversineDistance(
          latitude,
          longitude,
          parish.latitude,
          parish.longitude
        );
        return { ...parish, distance };
      })
      .filter((p): p is Parish & { distance: number } => p !== null && p.distance <= radiusMiles)
      .sort((a, b) => a.distance - b.distance)
      .slice(0, 100);

    return results;
  } catch (error) {
    console.error('Error searching parishes:', error);
    throw error;
  }
}
