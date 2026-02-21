import type { SortOption } from '../utils/sorting';
import { getSortLabel } from '../utils/sorting';

interface SortControlProps {
  sortBy: SortOption;
  onSortChange: (option: SortOption) => void;
}

const SORT_OPTIONS: SortOption[] = ['distance', 'name', 'nextMass'];

export default function SortControl({ sortBy, onSortChange }: SortControlProps) {
  return (
    <div className="flex items-center gap-2">
      <label
        htmlFor="sort-select"
        className="text-xs font-medium uppercase tracking-wide text-gray-500"
      >
        Sort By
      </label>
      <select
        id="sort-select"
        value={sortBy}
        onChange={(e) => onSortChange(e.target.value as SortOption)}
        className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-200"
        aria-label="Sort parishes by"
      >
        {SORT_OPTIONS.map((option) => (
          <option key={option} value={option}>
            {getSortLabel(option)}
          </option>
        ))}
      </select>
    </div>
  );
}
