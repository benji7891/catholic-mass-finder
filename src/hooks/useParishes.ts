import { useState, useCallback } from 'react';
import { searchCatholicChurches } from '../services/overpass';
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
      const parishes = await retryWithBackoff(() => searchCatholicChurches(lat, lng), 3, 1000);
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
