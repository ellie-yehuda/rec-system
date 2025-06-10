/**
 * Custom hook for making API requests with built-in loading and error states.
 * 
 * Features:
 * - Automatic loading state management
 * - Error handling
 * - Configurable request options
 * - Type-safe response handling
 */
import { useState, useCallback } from 'react';

// API base URL from environment variables, fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';

/**
 * Return type for the useApi hook
 * 
 * @template T The expected type of the API response data
 * @property data - The API response data or null if not yet loaded
 * @property loading - Whether the request is in progress
 * @property error - Error object if the request failed, null otherwise
 * @property doFetch - Function to trigger the API request
 */
interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  doFetch: (options?: RequestInit) => void;
}

/**
 * Hook for making API requests with automatic state management.
 * 
 * @template T The expected type of the API response data
 * @param endpoint - The API endpoint to call (will be appended to API_BASE_URL)
 * @returns Object containing data, loading state, error state, and fetch trigger
 * 
 * @example
 * ```typescript
 * const { data, loading, error, doFetch } = useApi<User>('/api/user');
 * 
 * useEffect(() => {
 *   doFetch({ method: 'GET' });
 * }, []);
 * ```
 */
export function useApi<T>(endpoint: string): UseApiResult<T> {
  // State for storing the API response
  const [data, setData] = useState<T | null>(null);
  // Loading state indicator
  const [loading, setLoading] = useState<boolean>(false);
  // Error state storage
  const [error, setError] = useState<Error | null>(null);

  // Memoized fetch function to prevent unnecessary re-renders
  const doFetch = useCallback(async (options: RequestInit = {}) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setData(result);
    } catch (e) {
      setError(e as Error);
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  return { data, loading, error, doFetch };
} 