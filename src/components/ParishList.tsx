import type { Church } from '../types';
import ParishCard from './ParishCard';

interface ParishListProps {
  parishes: Church[];
  selectedId: number | null;
  onSelect: (church: Church) => void;
  isFiltered?: boolean;
}

export default function ParishList({ parishes, selectedId, onSelect, isFiltered = false }: ParishListProps) {
  if (parishes.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <svg className="h-12 w-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <p className="mt-3 text-sm font-medium text-gray-700">
          {isFiltered
            ? 'No parishes match your filters'
            : 'Search for a location to find nearby parishes'}
        </p>
        {isFiltered && (
          <p className="mt-1 text-xs text-gray-500">
            Try adjusting your day or service type filters
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <p className="text-sm text-gray-500">
        {parishes.length} parish{parishes.length !== 1 ? 'es' : ''} found
      </p>
      {parishes.map((church) => (
        <ParishCard
          key={church.id}
          church={church}
          isSelected={church.id === selectedId}
          onClick={() => onSelect(church)}
        />
      ))}
    </div>
  );
}
