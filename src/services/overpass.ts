import type { Church, WorshipTime } from '../types';

// Overpass API endpoint
const OVERPASS_API = 'https://overpass-api.de/api/interpreter';

interface OverpassElement {
  type: 'node' | 'way' | 'relation';
  id: number;
  lat?: number;
  lon?: number;
  center?: { lat: number; lon: number };
  tags?: {
    name?: string;
    'addr:street'?: string;
    'addr:housenumber'?: string;
    'addr:city'?: string;
    'addr:state'?: string;
    'addr:postcode'?: string;
    'addr:country'?: string;
    phone?: string;
    website?: string;
    'contact:phone'?: string;
    'contact:website'?: string;
    denomination?: string;
    religion?: string;
    // Mass times - rarely populated but worth trying
    'service_times'?: string;
    'mass_times'?: string;
    'opening_hours'?: string;
  };
}

interface OverpassResponse {
  elements: OverpassElement[];
}

/**
 * Calculate distance between two points using Haversine formula
 */
function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 3959; // Earth's radius in miles
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

/**
 * Parse mass times from OSM tags (if available)
 * Most churches don't have this data in OSM
 */
function parseWorshipTimes(element: OverpassElement): WorshipTime[] {
  const times: WorshipTime[] = [];
  const tags = element.tags;
  
  if (!tags) return times;

  // Try to parse mass_times tag if it exists
  if (tags.mass_times) {
    // OSM format varies, but try to parse common formats
    times.push({
      day: 'Unknown',
      time: tags.mass_times,
      type: 'Mass',
      note: 'From OpenStreetMap - verify with parish'
    });
  }

  // Try service_times
  if (tags.service_times) {
    times.push({
      day: 'Unknown',
      time: tags.service_times,
      type: 'Service',
      note: 'From OpenStreetMap - verify with parish'
    });
  }

  return times;
}

/**
 * Convert Overpass element to Church object
 */
function elementToChurch(element: OverpassElement, searchLat: number, searchLon: number): Church | null {
  const tags = element.tags;
  if (!tags || !tags.name) return null;

  // Get coordinates
  const lat = element.lat || element.center?.lat;
  const lon = element.lon || element.center?.lon;
  if (!lat || !lon) return null;

  // Build address
  const street = tags['addr:street'] || '';
  const houseNumber = tags['addr:housenumber'] || '';
  const address = houseNumber ? `${houseNumber} ${street}`.trim() : street;

  // Get phone and website (check both direct and contact: prefixed)
  const phone = tags.phone || tags['contact:phone'];
  const website = tags.website || tags['contact:website'];

  // Calculate distance
  const distance = calculateDistance(searchLat, searchLon, lat, lon);

  return {
    id: element.id,
    name: tags.name,
    address: address || '',
    city: tags['addr:city'] || '',
    state: tags['addr:state'] || '',
    zip: tags['addr:postcode'] || '',
    country: tags['addr:country'] || '',
    phone,
    url: website,
    latitude: lat,
    longitude: lon,
    distance,
    worshipTimes: parseWorshipTimes(element),
  };
}

/**
 * Search for Catholic churches near a location using Overpass API
 * @param lat Latitude
 * @param lng Longitude
 * @param radiusMeters Search radius in meters (default: 25km)
 * @returns Array of churches
 */
export async function searchCatholicChurches(
  lat: number,
  lng: number,
  radiusMeters: number = 25000
): Promise<Church[]> {
  // Build Overpass QL query
  // Search for places of worship with religion=christian and denomination=catholic
  const query = `
    [out:json][timeout:25];
    (
      node["amenity"="place_of_worship"]["religion"="christian"]["denomination"="catholic"](around:${radiusMeters},${lat},${lng});
      way["amenity"="place_of_worship"]["religion"="christian"]["denomination"="catholic"](around:${radiusMeters},${lat},${lng});
      relation["amenity"="place_of_worship"]["religion"="christian"]["denomination"="catholic"](around:${radiusMeters},${lat},${lng});
    );
    out center tags;
  `;

  try {
    const response = await fetch(OVERPASS_API, {
      method: 'POST',
      body: `data=${encodeURIComponent(query)}`,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    if (!response.ok) {
      throw new Error(`Overpass API error: ${response.statusText}`);
    }

    const data: OverpassResponse = await response.json();

    // Convert elements to Church objects
    const churches = data.elements
      .map(el => elementToChurch(el, lat, lng))
      .filter((church): church is Church => church !== null)
      .sort((a, b) => (a.distance || 0) - (b.distance || 0));

    return churches;

  } catch (error) {
    console.error('Overpass API error:', error);
    throw error;
  }
}
