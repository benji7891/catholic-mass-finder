import type { DayOfWeek, ServiceType } from '../types';
import { DAYS_OF_WEEK, SERVICE_TYPES } from '../types';

interface FilterBarProps {
  selectedDay: DayOfWeek | 'All';
  selectedService: ServiceType | 'All';
  onDayChange: (day: DayOfWeek | 'All') => void;
  onServiceChange: (service: ServiceType | 'All') => void;
}

export default function FilterBar({
  selectedDay,
  selectedService,
  onDayChange,
  onServiceChange,
}: FilterBarProps) {
  return (
    <div className="flex flex-wrap gap-3" role="group" aria-label="Filter parishes">
      <div className="flex items-center gap-2">
        <label htmlFor="filter-day" className="text-xs font-medium uppercase tracking-wide text-gray-500">Day</label>
        <select
          id="filter-day"
          value={selectedDay}
          onChange={(e) => onDayChange(e.target.value as DayOfWeek | 'All')}
          className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-200"
          aria-label="Filter by day of week"
        >
          <option value="All">All Days</option>
          {DAYS_OF_WEEK.map((day) => (
            <option key={day} value={day}>
              {day}
            </option>
          ))}
        </select>
      </div>
      <div className="flex items-center gap-2">
        <label htmlFor="filter-service" className="text-xs font-medium uppercase tracking-wide text-gray-500">Type</label>
        <select
          id="filter-service"
          value={selectedService}
          onChange={(e) => onServiceChange(e.target.value as ServiceType | 'All')}
          className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-200"
          aria-label="Filter by service type"
        >
          <option value="All">All Types</option>
          {SERVICE_TYPES.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
