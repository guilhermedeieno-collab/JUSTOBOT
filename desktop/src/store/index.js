import { create } from 'zustand';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/api/v1';

export const useStore = create((set, get) => ({
  // Estado
  config: {},
  apiUrl: API_BASE,
  tribunals: [],
  jobs: [],
  loading: false,
  error: null,

  // Inicialização
  initializeConfig: async () => {
    try {
      if (window.electron) {
        const config = await window.electron.config.getAll();
        const apiUrl = await window.electron.api.getUrl();
        set({ config, apiUrl: apiUrl + '/api/v1' });
      }
    } catch (error) {
      console.error('Error initializing config:', error);
    }
  },

  // Configuração
  setConfig: async (key, value) => {
    if (window.electron) {
      await window.electron.config.set(key, value);
    }
    set((state) => ({
      config: { ...state.config, [key]: value }
    }));
  },

  getConfig: async (key) => {
    if (window.electron) {
      return await window.electron.config.get(key);
    }
    return get().config[key];
  },

  // API Calls
  fetchTribunals: async () => {
    set({ loading: true, error: null });
    try {
      const response = await axios.get(`${get().apiUrl}/cases/tribunals`);
      set({ tribunals: response.data.tribunals, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  searchCases: async (tribunal, searchType, query) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${get().apiUrl}/cases/search`, {
        tribunal,
        search_type: searchType,
        query
      });
      set({ loading: false });
      return response.data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  uploadBulk: async (file, tribunal, searchType) => {
    set({ loading: true, error: null });
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('tribunal', tribunal);
      formData.append('search_type', searchType);

      const response = await axios.post(`${get().apiUrl}/bulk/upload`, formData);
      set({ loading: false });
      return response.data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  fetchJobStatus: async (jobId) => {
    try {
      const response = await axios.get(`${get().apiUrl}/bulk/status/${jobId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching job status:', error);
      return null;
    }
  },

  downloadResults: async (jobId) => {
    try {
      const response = await axios.get(`${get().apiUrl}/bulk/download/${jobId}`, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `justobot_results_${jobId}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading results:', error);
      throw error;
    }
  },

  fetchJobs: async () => {
    set({ loading: true, error: null });
    try {
      const response = await axios.get(`${get().apiUrl}/bulk/jobs`);
      set({ jobs: response.data.jobs, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  }
}));
