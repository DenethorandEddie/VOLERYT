import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 second timeout for searches
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Search for niches based on keyword and filters
 */
export const searchNiche = async (searchParams) => {
  try {
    const response = await apiClient.post('/api/v1/search/niche', searchParams);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Health check
 */
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/api/v1/health');
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Get quota information
 */
export const getQuotaInfo = async () => {
  try {
    const response = await apiClient.get('/api/v1/quota');
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Export results to CSV
 */
export const exportToCSV = async (channels) => {
  try {
    const response = await apiClient.post('/api/v1/export/csv', channels, {
      responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'niche_analysis.csv');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Export results to JSON
 */
export const exportToJSON = async (channels) => {
  try {
    const response = await apiClient.post('/api/v1/export/json', channels, {
      responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'niche_analysis.json');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Handle API errors consistently
 */
const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    const message = error.response.data?.detail || error.response.data?.error || 'Server error';
    return new Error(message);
  } else if (error.request) {
    // Request made but no response
    return new Error('No response from server. Please check your connection.');
  } else {
    // Error in request setup
    return new Error(error.message || 'An error occurred');
  }
};

export default apiClient;
