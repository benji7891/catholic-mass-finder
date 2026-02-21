import type { Church, WorshipTime } from '../types';

interface ApiWorshipTime {
  Day?: string;
  Time?: string;
  Type?: string;
  Language?: string;
  Note?: string;
}

interface ApiChurch {
  ChurchId?: number;
  Name?: string;
  Address?: string;
  City?: string;
  State?: string;
  Zip?: string;
  Country?: string;
  Phone?: string;
  Url?: string;
  Latitude?: number;
  Longitude?: number;
  Distance?: number;
  WorshipTimes?: ApiWorshipTime[];
}

function parseWorshipTime(raw: ApiWorshipTime): WorshipTime {
  return {
    day: raw.Day ?? '',
    time: raw.Time ?? '',
    type: raw.Type ?? '',
    language: raw.Language,
    note: raw.Note,
  };
}

function parseChurch(raw: ApiChurch): Church {
  return {
    id: raw.ChurchId ?? 0,
    name: raw.Name ?? 'Unknown Parish',
    address: raw.Address ?? '',
    city: raw.City ?? '',
    state: raw.State ?? '',
    zip: raw.Zip ?? '',
    country: raw.Country ?? '',
    phone: raw.Phone,
    url: raw.Url,
    latitude: raw.Latitude ?? 0,
    longitude: raw.Longitude ?? 0,
    distance: raw.Distance,
    worshipTimes: (raw.WorshipTimes ?? []).map(parseWorshipTime),
  };
}

/** Error with HTTP status for retry logic (don't retry 4xx) */
export class MassTimesApiError extends Error {
  readonly status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = 'MassTimesApiError';
    this.status = status;
  }
}

export async function fetchParishes(lat: number, lng: number): Promise<Church[]> {
  // Use serverless function endpoint (works in both dev and production)
  const url = `/api/masstimes?lat=${lat}&lng=${lng}`;

  const response = await fetch(url);
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const message =
      (typeof data?.error === 'string' ? data.error : null) ||
      (typeof data?.message === 'string' ? data.message : null) ||
      `MassTimes API error: ${response.status} ${response.statusText}`;
    throw new MassTimesApiError(message, response.status);
  }

  // The API may return an array directly or nested under a property
  const churches: ApiChurch[] = Array.isArray(data) ? data : data.Churches ?? data.churches ?? [];

  return churches.map(parseChurch);
}
