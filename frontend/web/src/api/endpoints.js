import api from './client';

// ===== CONTEÚDO PÚBLICO =====
export const getNoticias = () => api.get('/conteudo/noticias');
export const getEventos = () => api.get('/conteudo/eventos');

// ===== MÉTRICAS =====
export const getMetricasGerais = () => api.get('/metrics/geral');
export const getDadosSensores = (limit = 10) => api.get(`/metrics/sensores?limit=${limit}`);

// ===== PRESENÇA =====
export const registrarPresenca = (data) => api.post('/presenca/registrar', data);

// ===== AUTENTICAÇÃO (A FUNÇÃO QUE ESTAVA FALTANDO) =====
export const login = (email, password) => api.post('/token', { email, password });

// ===== ADMIN (CRUD) =====
export const criarConteudo = (data) => api.post('/admin/conteudo', data);
export const listarConteudo = () => api.get('/admin/conteudo');
export const atualizarConteudo = (id, data) => api.put(`/admin/conteudo/${id}`, data);
export const deletarConteudo = (id) => api.delete(`/admin/conteudo/${id}`);