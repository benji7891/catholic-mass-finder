import { Handler, HandlerEvent } from '@netlify/functions';

const API_KEY = process.env.MASSTIMES_API_KEY;
const MASSTIMES_API_URL = 'https://apiv4.updateparishdata.org';

interface MassTimesResponse {
  statusCode: number;
  body: string;
  headers: {
    'Content-Type': string;
    'Access-Control-Allow-Origin': string;
    'Access-Control-Allow-Headers': string;
    'Access-Control-Allow-Methods': string;
  };
}

const corsHeaders = {
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
};

export const handler: Handler = async (event: HandlerEvent): Promise<MassTimesResponse> => {
  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: corsHeaders,
      body: '',
    };
  }

  // Only allow GET requests
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'Method not allowed' }),
    };
  }

  // Validate API key is configured
  if (!API_KEY) {
    console.error('MASSTIMES_API_KEY is not configured');
    return {
      statusCode: 500,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'Server configuration error' }),
    };
  }

  // Extract and validate query parameters
  const { lat, long, lng } = event.queryStringParameters || {};
  const longitude = long || lng;

  if (!lat || !longitude) {
    return {
      statusCode: 400,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'Missing required parameters: lat and long/lng' }),
    };
  }

  // Validate coordinates
  const latitude = parseFloat(lat);
  const longitudeNum = parseFloat(longitude);

  if (isNaN(latitude) || isNaN(longitudeNum)) {
    return {
      statusCode: 400,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'Invalid coordinates' }),
    };
  }

  if (latitude < -90 || latitude > 90 || longitudeNum < -180 || longitudeNum > 180) {
    return {
      statusCode: 400,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'Coordinates out of valid range' }),
    };
  }

  try {
    // Make request to MassTimes API
    const url = `${MASSTIMES_API_URL}/Churchs/?lat=${latitude}&long=${longitudeNum}&apikey=${API_KEY}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`MassTimes API error: ${response.statusText}`);
    }

    const data = await response.json();

    return {
      statusCode: 200,
      headers: corsHeaders,
      body: JSON.stringify(data),
    };
  } catch (error) {
    console.error('Error fetching from MassTimes API:', error);
    return {
      statusCode: 500,
      headers: corsHeaders,
      body: JSON.stringify({ 
        error: 'Failed to fetch parishes',
        message: error instanceof Error ? error.message : 'Unknown error'
      }),
    };
  }
};
