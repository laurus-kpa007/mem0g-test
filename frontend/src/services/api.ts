import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 채팅 API
export const chatAPI = {
  sendMessage: (message: string, userId: string, sessionId?: string) =>
    api.post('/api/chat', { message, user_id: userId, session_id: sessionId }),
};

// 메모리 API
export const memoryAPI = {
  search: (query: string, userId: string, limit: number = 10) =>
    api.post('/api/memories/search', { query, user_id: userId, limit }),

  getAll: (userId: string, limit: number = 100) =>
    api.get('/api/memories', { params: { user_id: userId, limit } }),

  delete: (memoryId: string) =>
    api.delete(`/api/memories/${memoryId}`),

  deleteAll: (userId: string) =>
    api.delete('/api/memories', { params: { user_id: userId } }),
};

// 그래프 API
export const graphAPI = {
  getStats: (userId?: string) =>
    api.get('/api/graph/stats', { params: userId ? { user_id: userId } : {} }),

  visualize: (userId: string, limit: number = 100) =>
    api.get('/api/graph/visualize', { params: { user_id: userId, limit } }),
};

// 테스트 API
export const testAPI = {
  extractEntities: (text: string) =>
    api.post('/api/test/entity-extraction', { text }),

  runBenchmark: () =>
    api.get('/api/test/benchmark'),
};

// 관리자 API
export const adminAPI = {
  health: () =>
    api.get('/api/admin/health'),

  getConfig: () =>
    api.get('/api/admin/config'),

  reset: () =>
    api.post('/api/admin/reset', {}, { params: { confirm: true } }),
};
