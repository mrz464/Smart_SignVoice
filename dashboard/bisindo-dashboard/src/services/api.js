import axios from 'axios';

// Di server: '/api' (diteruskan nginx ke backend).
// Saat dijalankan lokal (npm start): isi REACT_APP_API_URL=http://localhost:8000 di file .env.local
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Sertakan token login di setiap permintaan
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Token habis atau tidak valid: hapus sesi dan kembali ke halaman login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const diLogin = window.location.pathname === '/login';
    if ((status === 401 || status === 403) && !diLogin) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const login = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data;
};

export const getDashboardStats = async () => {
  const response = await api.get('/dashboard/stats');
  return response.data;
};

export const getSessions = async () => {
  const response = await api.get('/sessions');
  return response.data;
};

export default api;