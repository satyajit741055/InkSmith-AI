import axios from 'axios';

// Determine API base URL dynamically
let API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  // If not set in .env, construct from current window location
  const protocol = window.location.protocol;
  const hostname = window.location.hostname;
  const port = 8001;
  API_BASE_URL = `${protocol}//${hostname}:${port}/api/v1`;
}

console.log('API Base URL:', API_BASE_URL);

const client = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default client;
