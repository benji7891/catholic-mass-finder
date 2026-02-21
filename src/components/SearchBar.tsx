import { useState } from 'react';
import { validateSearchQuery, sanitizeInput } from '../utils/validation';

interface SearchBarProps {
  onSearch: (query: string) => void;
  onUseMyLocation: () => void;
  loading: boolean;
  geoLoading: boolean;
}

export default function SearchBar({ onSearch, onUseMyLocation, loading, geoLoading }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);
    
    const trimmed = query.trim();
    if (!trimmed) {
      setValidationError('Please enter a location');
      return;
    }
    
    const validation = validateSearchQuery(trimmed);
    if (!validation.valid) {
      setValidationError(validation.error || 'Invalid input');
      return;
    }
    
    const sanitized = sanitizeInput(trimmed);
    onSearch(sanitized);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
    if (validationError) {
      setValidationError(null);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start">
        <div className="relative flex-1">
          <svg
            className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
          <input
            type="text"
            value={query}
            onChange={handleInputChange}
            placeholder="Enter zip code or city name..."
            className={`w-full rounded-lg border bg-white py-2.5 pl-10 pr-4 text-sm shadow-sm focus:outline-none focus:ring-2 ${
              validationError
                ? 'border-red-300 focus:border-red-500 focus:ring-red-200'
                : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-200'
            }`}
            aria-invalid={!!validationError}
            aria-describedby={validationError ? 'search-error' : undefined}
          />
        </div>
      <div className="flex gap-2">
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
        <button
          type="button"
          onClick={onUseMyLocation}
          disabled={geoLoading}
          className="flex items-center gap-1.5 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          {geoLoading ? 'Locating...' : 'Use My Location'}
        </button>
      </div>
      </div>
      {validationError && (
        <p id="search-error" className="text-sm text-red-600" role="alert">
          {validationError}
        </p>
      )}
    </form>
  );
}
