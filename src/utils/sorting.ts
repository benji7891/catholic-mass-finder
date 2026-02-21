import type { Church, WorshipTime } from '../types';

export type SortOption = 'distance' | 'name' | 'nextMass';

/**
 * Get the next upcoming Mass time for a church
 */
function getNextMassTimestamp(worshipTimes: WorshipTime[]): number {
  const now = new Date();
  const currentDay = now.toLocaleString('en-US', { weekday: 'long' });
  const currentTime = now.getHours() * 60 + now.getMinutes();

  const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const currentDayIndex = daysOfWeek.indexOf(currentDay);

  const massTimes = worshipTimes.filter(wt => 
    wt.type.toLowerCase().includes('mass')
  );

  // Find next mass today or in upcoming days
  for (let dayOffset = 0; dayOffset < 7; dayOffset++) {
    const targetDayIndex = (currentDayIndex + dayOffset) % 7;
    const targetDay = daysOfWeek[targetDayIndex];

    const todayMasses = massTimes.filter(wt => wt.day === targetDay);
    
    for (const mass of todayMasses) {
      const timeMatch = mass.time.match(/(\d{1,2}):(\d{2})\s*(AM|PM)?/i);
      if (!timeMatch) continue;

      let hours = parseInt(timeMatch[1]);
      const minutes = parseInt(timeMatch[2]);
      const period = timeMatch[3]?.toUpperCase();

      if (period === 'PM' && hours !== 12) hours += 12;
      if (period === 'AM' && hours === 12) hours = 0;

      const massTime = hours * 60 + minutes;

      // If it's today, only count masses that haven't happened yet
      if (dayOffset === 0 && massTime <= currentTime) continue;

      return dayOffset * 1440 + massTime; // Return minutes from now
    }
  }

  return Number.MAX_SAFE_INTEGER; // No mass found
}

/**
 * Sort parishes by the specified criterion
 */
export function sortParishes(parishes: Church[], sortBy: SortOption): Church[] {
  const sorted = [...parishes];

  switch (sortBy) {
    case 'distance':
      sorted.sort((a, b) => {
        const distA = a.distance ?? Number.MAX_SAFE_INTEGER;
        const distB = b.distance ?? Number.MAX_SAFE_INTEGER;
        return distA - distB;
      });
      break;

    case 'name':
      sorted.sort((a, b) => a.name.localeCompare(b.name));
      break;

    case 'nextMass':
      sorted.sort((a, b) => {
        const timeA = getNextMassTimestamp(a.worshipTimes);
        const timeB = getNextMassTimestamp(b.worshipTimes);
        return timeA - timeB;
      });
      break;
  }

  return sorted;
}

/**
 * Get display label for sort option
 */
export function getSortLabel(sortBy: SortOption): string {
  switch (sortBy) {
    case 'distance':
      return 'Distance';
    case 'name':
      return 'Name';
    case 'nextMass':
      return 'Next Mass';
    default:
      return 'Distance';
  }
}
