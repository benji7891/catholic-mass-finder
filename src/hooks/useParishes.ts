import { useState, useCallback } from 'react';
import { searchParishes } from '../services/localParishes';
import type { Church } from '../types';
import { retryWithBackoff, getErrorMessage } from '../utils/retry';
import { getCachedParishes, cacheParishes } from '../utils/cache';

interface ParishesState {
  parishes: Church[];
  loading: boolean;
  error: string | null;
}

export function useParishes() {
  const [state, setState] = useState<ParishesState>({
    parishes: [],
    loading: false,
    error: null,
  });

  const search = useCallback(async (lat: number, lng: number) => {
    // Check cache first
    const cached = getCachedParishes(lat, lng);
    if (cached) {
      setState({ parishes: cached, loading: false, error: null });
      return cached;
    }

    setState({ parishes: [], loading: true, error: null });

    try {
      const results = await retryWithBackoff(() => searchParishes(lat, lng, 50), 3, 1000);
      // Map local DB results to Church format
      const parishes: Church[] = results.map(p => ({
        id: p.id,
        name: p.name,
        address: p.address,
        city: p.city,
        state: p.state,
        zip: p.zip,
        country: p.country,
        latitude: p.latitude,
        longitude: p.longitude,
        phone: p.phone,
        url: p.website,
        distance: p.distance,
        worshipTimes: [],  // Can be enhanced later when we scrape mass times
      }));
      cacheParishes(lat, lng, parishes);
      setState({ parishes, loading: false, error: null });
      return parishes;
    } catch (err) {
      const message = getErrorMessage(err);
      setState({ parishes: [], loading: false, error: message });
      return [];
    }
  }, []);

  return { ...state, search };
}
