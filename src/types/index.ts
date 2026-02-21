export interface WorshipTime {
  day: string;
  time: string;
  type: string;
  language?: string;
  note?: string;
}

export interface Church {
  id: number;
  name: string;
  address: string;
  city: string;
  state: string;
  zip: string;
  country: string;
  phone?: string;
  url?: string;
  latitude: number;
  longitude: number;
  distance?: number;
  worshipTimes: WorshipTime[];
}

export interface GeocodingResult {
  lat: number;
  lng: number;
  displayName: string;
}

export type ServiceType = 'Mass' | 'Confession' | 'Adoration' | 'All';

export type DayOfWeek =
  | 'Sunday'
  | 'Monday'
  | 'Tuesday'
  | 'Wednesday'
  | 'Thursday'
  | 'Friday'
  | 'Saturday'
  | 'All';

export const DAYS_OF_WEEK: DayOfWeek[] = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
];

export const SERVICE_TYPES: ServiceType[] = ['Mass', 'Confession', 'Adoration'];
