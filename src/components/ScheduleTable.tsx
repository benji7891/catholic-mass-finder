import type { WorshipTime } from '../types';
import { DAYS_OF_WEEK } from '../types';

interface ScheduleTableProps {
  worshipTimes: WorshipTime[];
}

function getServiceColor(type: string): string {
  const t = type.toLowerCase();
  if (t.includes('mass')) return 'bg-indigo-100 text-indigo-800';
  if (t.includes('confession') || t.includes('reconciliation')) return 'bg-purple-100 text-purple-800';
  if (t.includes('adoration')) return 'bg-amber-100 text-amber-800';
  return 'bg-gray-100 text-gray-800';
}

export default function ScheduleTable({ worshipTimes }: ScheduleTableProps) {
  if (worshipTimes.length === 0) {
    return <p className="text-sm text-gray-500 italic">No schedule information available.</p>;
  }

  // Group by day
  const byDay = new Map<string, WorshipTime[]>();
  for (const wt of worshipTimes) {
    const day = wt.day || 'Other';
    if (!byDay.has(day)) byDay.set(day, []);
    byDay.get(day)!.push(wt);
  }

  // Sort days in weekday order
  const sortedDays = [...byDay.keys()].sort((a, b) => {
    const ia = DAYS_OF_WEEK.indexOf(a as any);
    const ib = DAYS_OF_WEEK.indexOf(b as any);
    return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib);
  });

  return (
    <div className="space-y-3">
      {sortedDays.map((day) => (
        <div key={day}>
          <h4 className="text-sm font-semibold text-gray-700 mb-1">{day}</h4>
          <div className="space-y-1">
            {byDay.get(day)!.map((wt, i) => (
              <div key={i} className="flex items-center gap-2 text-sm">
                <span
                  className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${getServiceColor(wt.type)}`}
                >
                  {wt.type}
                </span>
                <span className="text-gray-900">{wt.time}</span>
                {wt.language && (
                  <span className="text-gray-400 text-xs">({wt.language})</span>
                )}
                {wt.note && (
                  <span className="text-gray-400 text-xs italic">- {wt.note}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
