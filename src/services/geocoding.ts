import type { GeocodingResult } from '../types';
import { validateCoordinates } from '../utils/validation';

const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search';

export async function geocodeLocation(query: string): Promise<GeocodingResult | null> {
  const params = new URLSearchParams({
    q: query,
    format: 'json',
    limit: '1',
    // Removed countrycodes restriction to allow international searches
  });

  const response = await fetch(`${NOMINATIM_URL}?${params}`, {
    headers: {
      'User-Agent': 'CatholicMassFinder/1.0',
    },
  });

  if (!response.ok) {
    throw new Error(`Geocoding failed: ${response.statusText}`);
  }

  const results = await response.json();

  if (results.length === 0) {
    return null;
  }

  const result = results[0];
  const lat = parseFloat(result.lat);
  const lng = parseFloat(result.lon);
  
  // Validate coordinates
  const validation = validateCoordinates(lat, lng);
  if (!validation.valid) {
    throw new Error(validation.error || 'Invalid coordinates returned');
  }
  
  return {
    lat,
    lng,
    displayName: result.display_name,
  };
}
