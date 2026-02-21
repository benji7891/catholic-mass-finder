import { useState, useCallback } from 'react';
import { geocodeLocation } from '../services/geocoding';
import type { GeocodingResult } from '../types';
import { retryWithBackoff, getErrorMessage } from '../utils/retry';
import { getCachedGeocodingResult, cacheGeocodingResult } from '../utils/cache';

interface GeocodingState {
  result: GeocodingResult | null;
  loading: boolean;
  error: string | null;
}

export function useGeocoding() {
  const [state, setState] = useState<GeocodingState>({
    result: null,
    loading: false,
    error: null,
  });

  const geocode = useCallback(async (query: string) => {
    // Check cache first
    const cached = getCachedGeocodingResult(query);
    if (cached) {
      setState({ result: cached, loading: false, error: null });
      return cached;
    }

    setState({ result: null, loading: true, error: null });

    try {
      const result = await retryWithBackoff(() => geocodeLocation(query), 2, 500);
      if (!result) {
        const message = 'Location not found. Try a different zip code or city name.';
        setState({ result: null, loading: false, error: message });
        cacheGeocodingResult(query, null);
        return null;
      }
      cacheGeocodingResult(query, result);
      setState({ result, loading: false, error: null });
      return result;
    } catch (err) {
      const message = getErrorMessage(err);
      setState({ result: null, loading: false, error: message });
      return null;
    }
  }, []);

  return { ...state, geocode };
}
