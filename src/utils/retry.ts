/**
 * Retry a promise-based function with exponential backoff
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  initialDelay: number = 1000
): Promise<T> {
  let lastError: Error;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error('Unknown error');
      
      // Don't retry on last attempt
      if (attempt === maxRetries) {
        break;
      }
      
      // Don't retry on client errors (4xx) - check for status on error object
      const status = (error as Error & { status?: number }).status;
      if (typeof status === 'number' && status >= 400 && status < 500) {
        throw lastError;
      }
      
      // Calculate delay with exponential backoff
      const delay = initialDelay * Math.pow(2, attempt);
      const jitter = Math.random() * 0.3 * delay; // Add 0-30% jitter
      
      console.log(`Retry attempt ${attempt + 1}/${maxRetries} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay + jitter));
    }
  }
  
  throw lastError!;
}

/**
 * Check if an error is a network error that should be retried
 */
export function isNetworkError(error: unknown): boolean {
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return true;
  }
  
  if (error instanceof Error) {
    const message = error.message.toLowerCase();
    return (
      message.includes('network') ||
      message.includes('timeout') ||
      message.includes('connection') ||
      message.includes('econnrefused')
    );
  }
  
  return false;
}

/**
 * Get user-friendly error message
 */
export function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    // Network errors
    if (isNetworkError(error)) {
      return 'Unable to connect. Please check your internet connection and try again.';
    }
    
    // API errors (4xx from proxy show user message; 5xx generic)
    const status = (error as Error & { status?: number }).status;
    if (typeof status === 'number' && status >= 400 && status < 500) {
      return error.message.length < 120 ? error.message : 'Invalid request. Please try a different location.';
    }
    if (error.message.includes('API error') || error.message.includes('Failed to fetch')) {
      return 'Service temporarily unavailable. Please try again in a moment.';
    }
    
    // Geocoding errors
    if (error.message.includes('Location not found')) {
      return 'Location not found. Try a different zip code or city name.';
    }
    
    // Return original message if it seems user-friendly
    if (error.message.length < 100 && !error.message.includes('undefined')) {
      return error.message;
    }
  }
  
  return 'An unexpected error occurred. Please try again.';
}
