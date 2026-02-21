/**
 * Sanitize user input to prevent XSS attacks
 * Removes potentially dangerous characters while preserving useful input
 */
export function sanitizeInput(input: string): string {
  return input
    .trim()
    .replace(/[<>'"]/g, '') // Remove common XSS characters
    .replace(/javascript:/gi, '') // Remove javascript: protocol
    .replace(/on\w+=/gi, ''); // Remove event handlers
}

/**
 * Validate search query input
 */
export function validateSearchQuery(query: string): { valid: boolean; error?: string } {
  const sanitized = sanitizeInput(query);
  
  if (!sanitized) {
    return { valid: false, error: 'Please enter a location' };
  }
  
  if (sanitized.length < 2) {
    return { valid: false, error: 'Location must be at least 2 characters' };
  }
  
  if (sanitized.length > 200) {
    return { valid: false, error: 'Location is too long' };
  }
  
  // Check for suspicious patterns
  if (/[{}[\]\\]/.test(sanitized)) {
    return { valid: false, error: 'Invalid characters in location' };
  }
  
  return { valid: true };
}

/**
 * Validate coordinates
 */
export function validateCoordinates(lat: number, lng: number): { valid: boolean; error?: string } {
  if (isNaN(lat) || isNaN(lng)) {
    return { valid: false, error: 'Invalid coordinates' };
  }
  
  if (lat < -90 || lat > 90) {
    return { valid: false, error: 'Latitude must be between -90 and 90' };
  }
  
  if (lng < -180 || lng > 180) {
    return { valid: false, error: 'Longitude must be between -180 and 180' };
  }
  
  return { valid: true };
}

/**
 * Sanitize URL to prevent open redirect attacks
 */
export function sanitizeUrl(url: string): string {
  const sanitized = sanitizeInput(url);
  
  // Only allow http and https protocols
  if (!sanitized.match(/^https?:\/\//i)) {
    return `https://${sanitized}`;
  }
  
  return sanitized;
}
