import axios, { AxiosResponse } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API functions
export const authAPI = {
  register: (userData: { email: string; password: string; name?: string }) =>
    api.post('/auth/register', userData),

  login: (credentials: { email: string; password: string }) =>
    api.post('/auth/login', credentials),

  logout: () => {
    localStorage.removeItem('access_token');
    return Promise.resolve({ data: { message: 'Logged out successfully' } });
  },

  getCurrentUser: () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      return Promise.reject(new Error('No token found'));
    }
    // We'll decode the token to get user info without making an API call
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return Promise.resolve({ data: JSON.parse(jsonPayload) });
    } catch (error) {
      return Promise.reject(error);
    }
  },
};

// Task API functions
export const taskAPI = {
  getAll: (params?: { completed?: boolean; priority?: string; search?: string }) =>
    api.get('/tasks', { params }),

  create: (taskData: { title: string; description?: string; priority?: string; due_date?: string }) =>
    api.post('/tasks', taskData),

  update: (id: number, taskData: { title?: string; description?: string; priority?: string; due_date?: string; completed?: boolean }) =>
    api.put(`/tasks/${id}`, taskData),

  delete: (id: number) => api.delete(`/tasks/${id}`),

  toggleComplete: (id: number) => api.patch(`/tasks/${id}/complete`),
};

export default api;