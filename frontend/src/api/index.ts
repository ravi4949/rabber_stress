import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  login: (credentials: { email: string; password: string }) => 
    apiClient.post('/auth/login', credentials),
    
  register: (user: { email: string; password: string; full_name: string }) => 
    apiClient.post('/auth/register', user),
    
  uploadCsv: (formData: FormData) => 
    apiClient.post('/uploads/csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
    
  submitJob: (data: { model_type: string; material_name: string }) => 
    apiClient.post('/jobs/submit', data),
    
  getJobStatus: (jobId: string) => 
    apiClient.get(`/jobs/${jobId}/status`),
    
  getResults: (jobId: string) => 
    apiClient.get(`/results/${jobId}`),
    
  getMaterials: () => 
    apiClient.get('/materials'),
};
