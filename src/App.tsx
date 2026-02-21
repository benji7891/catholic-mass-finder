import { useState, useEffect, useCallback, useMemo } from 'react';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import FilterBar from './components/FilterBar';
import SortControl from './components/SortControl';
import ParishList from './components/ParishList';
import ParishDetail from './components/ParishDetail';
import MapView from './components/MapView';
import { ParishSkeletonList } from './components/ParishSkeleton';
import { useGeocoding } from './hooks/useGeocoding';
import { useParishes } from './hooks/useParishes';
import { useGeolocation } from './hooks/useGeolocation';
import { sortParishes, type SortOption } from './utils/sorting';
import type { Church, DayOfWeek, ServiceType } from './types';

type MobileView = 'list' | 'map';

export default function App() {
  const { geocode, loading: geoLoading } = useGeocoding();
  const { parishes, loading: parishLoading, error: parishError, search } = useParishes();
  const {
    lat: geoLat,
    lng: geoLng,
    loading: locLoading,
    error: locError,
    requestLocation,
  } = useGeolocation();

  const [selectedChurch, setSelectedChurch] = useState<Church | null>(null);
  const [mapCenter, setMapCenter] = useState<[number, number] | null>(null);
  const [filterDay, setFilterDay] = useState<DayOfWeek | 'All'>('All');
  const [filterService, setFilterService] = useState<ServiceType | 'All'>('All');
  const [sortBy, setSortBy] = useState<SortOption>('distance');
  const [mobileView, setMobileView] = useState<MobileView>('list');
  const [searchError, setSearchError] = useState<string | null>(null);

  const handleSearch = useCallback(
    async (query: string) => {
      setSearchError(null);
      setSelectedChurch(null);
      const result = await geocode(query);
      if (result) {
        setMapCenter([result.lat, result.lng]);
        await search(result.lat, result.lng);
      } else {
        setSearchError('Could not find that location. Try a zip code or city name.');
      }
    },
    [geocode, search]
  );

  const handleUseMyLocation = useCallback(() => {
    setSearchError(null);
    setSelectedChurch(null);
    requestLocation();
  }, [requestLocation]);

  // When browser geolocation resolves, search for parishes
  useEffect(() => {
    if (geoLat != null && geoLng != null) {
      setMapCenter([geoLat, geoLng]);
      search(geoLat, geoLng);
    }
  }, [geoLat, geoLng, search]);

  const handleSelectChurch = useCallback((church: Church) => {
    const newChurch = selectedChurch?.id === church.id ? null : church;
    setSelectedChurch(newChurch);
    
    // On mobile, switch to list view when selecting a church to show details
    if (newChurch && window.innerWidth < 768) {
      setMobileView('list');
    }
  }, [selectedChurch]);

  // Filter and sort parishes
  const filteredAndSortedParishes = useMemo(() => {
    // First filter
    const filtered =
      filterDay === 'All' && filterService === 'All'
        ? parishes
        : parishes.filter((p) =>
            p.worshipTimes.some((wt) => {
              if (filterDay !== 'All' && wt.day !== filterDay) return false;
              if (filterService !== 'All') {
                const t = wt.type.toLowerCase();
                const f = filterService.toLowerCase();
                if (!t.includes(f) && !(f === 'confession' && t.includes('reconciliation')))
                  return false;
              }
              return true;
            })
          );
    
    // Then sort
    return sortParishes(filtered, sortBy);
  }, [parishes, filterDay, filterService, sortBy]);

  const loading = geoLoading || parishLoading || locLoading;
  const error = searchError || parishError || locError;

  return (
    <div className="flex h-screen flex-col">
      <Header />

      {/* Search + Filters */}
      <div className="border-b border-gray-200 bg-white px-4 py-3 shadow-sm">
        <div className="mx-auto max-w-7xl space-y-3">
          <SearchBar
            onSearch={handleSearch}
            onUseMyLocation={handleUseMyLocation}
            loading={loading}
            geoLoading={locLoading}
          />
          {parishes.length > 0 && (
            <div className="flex flex-wrap gap-3">
              <FilterBar
                selectedDay={filterDay}
                selectedService={filterService}
                onDayChange={setFilterDay}
                onServiceChange={setFilterService}
              />
              <SortControl sortBy={sortBy} onSortChange={setSortBy} />
            </div>
          )}
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border-b border-red-200 px-4 py-2">
          <p className="mx-auto max-w-7xl text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Mobile view toggle */}
      {parishes.length > 0 && (
        <div className="flex border-b border-gray-200 bg-white md:hidden">
          <button
            onClick={() => setMobileView('list')}
            className={`flex-1 py-2.5 text-center text-sm font-medium ${
              mobileView === 'list'
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-500'
            }`}
          >
            List ({filteredAndSortedParishes.length})
          </button>
          <button
            onClick={() => setMobileView('map')}
            className={`flex-1 py-2.5 text-center text-sm font-medium ${
              mobileView === 'map'
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-500'
            }`}
          >
            Map
          </button>
        </div>
      )}

      {/* Main content: list + map */}
      <main id="main-content" className="flex flex-1 overflow-hidden">
        {/* Left panel - List */}
        <div
          className={`flex-1 overflow-y-auto p-4 md:max-w-md md:border-r md:border-gray-200 lg:max-w-lg ${
            mobileView === 'map' && parishes.length > 0 ? 'hidden md:block' : ''
          }`}
          role="region"
          aria-label="Parish list and details"
        >
          {loading ? (
            <ParishSkeletonList count={5} />
          ) : selectedChurch ? (
            <ParishDetail
              church={selectedChurch}
              filterDay={filterDay}
              filterService={filterService}
              onClose={() => setSelectedChurch(null)}
            />
          ) : (
            <ParishList
              parishes={filteredAndSortedParishes}
              selectedId={null}
              onSelect={handleSelectChurch}
              isFiltered={filterDay !== 'All' || filterService !== 'All'}
            />
          )}
        </div>

        {/* Right panel - Map */}
        <div
          className={`flex-1 ${
            mobileView === 'list' && parishes.length > 0 ? 'hidden md:block' : ''
          }`}
          role="region"
          aria-label="Map view"
        >
          <MapView
            parishes={filteredAndSortedParishes}
            center={mapCenter}
            selectedId={selectedChurch?.id ?? null}
            onSelect={handleSelectChurch}
          />
        </div>
      </main>
    </div>
  );
}
