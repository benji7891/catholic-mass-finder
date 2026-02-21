import type { Church, WorshipTime } from '../types';

interface ParishCardProps {
  church: Church;
  isSelected: boolean;
  onClick: () => void;
}

function getNextMassTime(worshipTimes: WorshipTime[]): string | null {
  const massTimes = worshipTimes.filter((wt) =>
    wt.type.toLowerCase().includes('mass')
  );
  if (massTimes.length === 0) return null;

  // Find Sunday Mass or first available
  const sunday = massTimes.find((wt) => wt.day === 'Sunday');
  if (sunday) return `Sun ${sunday.time}`;
  return `${massTimes[0].day} ${massTimes[0].time}`;
}

export default function ParishCard({ church, isSelected, onClick }: ParishCardProps) {
  const nextMass = getNextMassTime(church.worshipTimes);
  const massCount = church.worshipTimes.filter((wt) =>
    wt.type.toLowerCase().includes('mass')
  ).length;
  const hasConfession = church.worshipTimes.some(
    (wt) => wt.type.toLowerCase().includes('confession') || wt.type.toLowerCase().includes('reconciliation')
  );
  const hasAdoration = church.worshipTimes.some((wt) =>
    wt.type.toLowerCase().includes('adoration')
  );

  return (
    <button
      onClick={onClick}
      aria-label={`View details for ${church.name}, ${church.distance != null ? `${church.distance.toFixed(1)} miles away` : ''}`}
      aria-pressed={isSelected}
      className={`w-full text-left rounded-lg border p-4 transition-all hover:shadow-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 ${
        isSelected
          ? 'border-indigo-500 bg-indigo-50 shadow-md ring-1 ring-indigo-500'
          : 'border-gray-200 bg-white hover:border-gray-300'
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-gray-900 leading-tight">{church.name}</h3>
        {church.distance != null && (
          <span className="shrink-0 rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600">
            {church.distance.toFixed(1)} mi
          </span>
        )}
      </div>
      <p className="mt-1 text-sm text-gray-500">
        {church.address}, {church.city}, {church.state} {church.zip}
      </p>

      {nextMass && (
        <p className="mt-2 text-sm">
          <span className="font-medium text-indigo-700">Next Mass:</span>{' '}
          <span className="text-gray-700">{nextMass}</span>
        </p>
      )}

      <div className="mt-2 flex flex-wrap gap-1.5">
        {massCount > 0 && (
          <span className="rounded-full bg-indigo-100 px-2 py-0.5 text-xs font-medium text-indigo-700">
            {massCount} Mass{massCount > 1 ? 'es' : ''}
          </span>
        )}
        {hasConfession && (
          <span className="rounded-full bg-purple-100 px-2 py-0.5 text-xs font-medium text-purple-700">
            Confession
          </span>
        )}
        {hasAdoration && (
          <span className="rounded-full bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-700">
            Adoration
          </span>
        )}
      </div>
    </button>
  );
}
