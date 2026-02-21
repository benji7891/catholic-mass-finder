import { Handler, HandlerEvent, HandlerContext } from '@netlify/functions';
import Database from 'better-sqlite3';
import path from 'path';

// Haversine distance calculation in SQL
const SEARCH_QUERY = `
  SELECT *,
    (3959 * acos(
      cos(radians(?)) * cos(radians(latitude)) *
      cos(radians(longitude) - radians(?)) +
      sin(radians(?)) * sin(radians(latitude))
    )) AS distance
  FROM parishes
  WHERE latitude IS NOT NULL
    AND longitude IS NOT NULL
  HAVING distance < ?
  ORDER BY distance
  LIMIT 100
`;

const handler: Handler = async (event: HandlerEvent, context: HandlerContext) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': 'https://catholic-mass-finder.netlify.app',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
  };

  // Handle preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: '',
    };
  }

  try {
    const { lat, lng, radius = '25' } = event.queryStringParameters || {};

    if (!lat || !lng) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Missing lat or lng parameters' }),
      };
    }

    const latitude = parseFloat(lat);
    const longitude = parseFloat(lng);
    const searchRadius = parseFloat(radius);

    if (isNaN(latitude) || isNaN(longitude) || isNaN(searchRadius)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid lat, lng, or radius' }),
      };
    }

    // Open database
    const dbPath = path.join(__dirname, 'parishes.db');
    const db = new Database(dbPath, { readonly: true, fileMustExist: true });

    // Query parishes
    const stmt = db.prepare(SEARCH_QUERY);
    const results = stmt.all(latitude, longitude, latitude, searchRadius);

    db.close();

    // Transform results to match app format
    const parishes = results.map((row: any) => ({
      id: row.id,
      name: row.name,
      diocese: row.diocese,
      address: row.address,
      city: row.city,
      state: row.state,
      zip: row.zip,
      country: row.country,
      phone: row.phone,
      website: row.website,
      email: row.email,
      latitude: row.latitude,
      longitude: row.longitude,
      distance: row.distance,
      massTimesText: row.mass_times,
    }));

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(parishes),
    };
  } catch (error) {
    console.error('Error querying parishes:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Internal server error',
        message: error instanceof Error ? error.message : 'Unknown error'
      }),
    };
  }
};

export { handler };
