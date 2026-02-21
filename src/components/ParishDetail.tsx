import type { Church, DayOfWeek, ServiceType } from '../types';
import ScheduleTable from './ScheduleTable';
import { sanitizeUrl } from '../utils/validation';

interface ParishDetailProps {
  church: Church;
  filterDay: DayOfWeek | 'All';
  filterService: ServiceType | 'All';
  onClose: () => void;
}

export default function ParishDetail({ church, filterDay, filterService, onClose }: ParishDetailProps) {
  const filteredTimes = church.worshipTimes.filter((wt) => {
    if (filterDay !== 'All' && wt.day !== filterDay) return false;
    if (filterService !== 'All') {
      const t = wt.type.toLowerCase();
      const f = filterService.toLowerCase();
      if (!t.includes(f) && !(f === 'confession' && t.includes('reconciliation'))) return false;
    }
    return true;
  });

  const handleGetDirections = () => {
    const address = `${church.address}, ${church.city}, ${church.state} ${church.zip}`;
    const encodedAddress = encodeURIComponent(address);
    
    // Check if on iOS/macOS for Apple Maps, otherwise use Google Maps
    const isApple = /iPhone|iPad|iPod|Macintosh/.test(navigator.userAgent);
    const url = isApple
      ? `http://maps.apple.com/?daddr=${encodedAddress}`
      : `https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`;
    
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return (
    <article className="rounded-lg border border-gray-200 bg-white p-5 shadow-lg" role="region" aria-label="Parish details">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-bold text-gray-900" id="parish-name">{church.name}</h2>
          <p className="mt-1 text-sm text-gray-500">
            {church.address}, {church.city}, {church.state} {church.zip}
          </p>
        </div>
        <button
          onClick={onClose}
          className="shrink-0 rounded-md p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          aria-label="Close parish details"
        >
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-sm text-gray-600">
        {church.phone && (
          <a href={`tel:${church.phone}`} className="flex items-center gap-1 hover:text-indigo-600">
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            {church.phone}
          </a>
        )}
        {church.url && (
          <a
            href={sanitizeUrl(church.url)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 hover:text-indigo-600"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            Website
          </a>
        )}
        {church.distance != null && (
          <span className="flex items-center gap-1">
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            </svg>
            {church.distance.toFixed(1)} miles away
          </span>
        )}
      </div>

      <hr className="my-4 border-gray-200" />

      <button
        onClick={handleGetDirections}
        className="w-full flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
        aria-label={`Get directions to ${church.name}`}
      >
        <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"
          />
        </svg>
        Get Directions
      </button>

      <hr className="my-4 border-gray-200" />

      <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500" id="schedule-heading">Schedule</h3>
      <ScheduleTable worshipTimes={filteredTimes} aria-labelledby="schedule-heading" />
    </article>
  );
}
