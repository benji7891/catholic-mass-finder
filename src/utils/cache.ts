import type { Church, GeocodingResult } from '../types';

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  expiresIn: number;
}

const CACHE_PREFIX = 'catholic-mass-finder-';
const DEFAULT_TTL = 30 * 60 * 1000; // 30 minutes

/**
 * Generate a cache key from parameters
 */
function generateKey(type: string, params: Record<string, unknown>): string {
  const sortedParams = Object.keys(params)
    .sort()
    .map(key => `${key}:${JSON.stringify(params[key])}`)
    .join('|');
  return `${CACHE_PREFIX}${type}:${sortedParams}`;
}

/**
 * Save data to cache
 */
function setCache<T>(key: string, data: T, ttl: number = DEFAULT_TTL): void {
  try {
    const entry: CacheEntry<T> = {
      data,
      timestamp: Date.now(),
      expiresIn: ttl,
    };
    localStorage.setItem(key, JSON.stringify(entry));
  } catch (error) {
    // Ignore localStorage errors (e.g., quota exceeded)
    console.warn('Cache write failed:', error);
  }
}

/**
 * Get data from cache if not expired
 */
function getCache<T>(key: string): T | null {
  try {
    const item = localStorage.getItem(key);
    if (!item) return null;

    const entry: CacheEntry<T> = JSON.parse(item);
    const age = Date.now() - entry.timestamp;

    if (age > entry.expiresIn) {
      localStorage.removeItem(key);
      return null;
    }

    return entry.data;
  } catch (error) {
    console.warn('Cache read failed:', error);
    return null;
  }
}

/**
 * Cache geocoding results
 */
export function cacheGeocodingResult(query: string, result: GeocodingResult | null): void {
  const key = generateKey('geocode', { query: query.toLowerCase().trim() });
  setCache(key, result, 24 * 60 * 60 * 1000); // 24 hours
}

/**
 * Get cached geocoding result
 */
export function getCachedGeocodingResult(query: string): GeocodingResult | null {
  const key = generateKey('geocode', { query: query.toLowerCase().trim() });
  return getCache<GeocodingResult>(key);
}

/**
 * Cache parish search results
 */
export function cacheParishes(lat: number, lng: number, parishes: Church[]): void {
  // Round coordinates to 3 decimal places (~110m precision)
  const roundedLat = Math.round(lat * 1000) / 1000;
  const roundedLng = Math.round(lng * 1000) / 1000;
  const key = generateKey('parishes', { lat: roundedLat, lng: roundedLng });
  setCache(key, parishes, 15 * 60 * 1000); // 15 minutes
}

/**
 * Get cached parish search results
 */
export function getCachedParishes(lat: number, lng: number): Church[] | null {
  const roundedLat = Math.round(lat * 1000) / 1000;
  const roundedLng = Math.round(lng * 1000) / 1000;
  const key = generateKey('parishes', { lat: roundedLat, lng: roundedLng });
  return getCache<Church[]>(key);
}

/**
 * Clear all cached data
 */
export function clearCache(): void {
  try {
    const keys = Object.keys(localStorage);
    keys.forEach(key => {
      if (key.startsWith(CACHE_PREFIX)) {
        localStorage.removeItem(key);
      }
    });
  } catch (error) {
    console.warn('Cache clear failed:', error);
  }
}

/**
 * Clear expired cache entries
 */
export function clearExpiredCache(): void {
  try {
    const keys = Object.keys(localStorage);
    keys.forEach(key => {
      if (key.startsWith(CACHE_PREFIX)) {
        const item = localStorage.getItem(key);
        if (item) {
          try {
            const entry: CacheEntry<unknown> = JSON.parse(item);
            const age = Date.now() - entry.timestamp;
            if (age > entry.expiresIn) {
              localStorage.removeItem(key);
            }
          } catch {
            // Invalid entry, remove it
            localStorage.removeItem(key);
          }
        }
      }
    });
  } catch (error) {
    console.warn('Cache cleanup failed:', error);
  }
}
