// API Configuration and HTTP Client
// Dashboard Sabrina Blogueira

const API_CONFIG = {
    baseURL: 'http://localhost:3000/api', // Alterar para produção
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json'
    }
};

// API Client Class
class APIClient {
    constructor(config) {
        this.baseURL = config.baseURL;
        this.timeout = config.timeout;
        this.headers = config.headers;
    }

    // Get authorization token
    getToken() {
        return localStorage.getItem('token');
    }

    // Build headers with authorization
    buildHeaders(customHeaders = {}) {
        const token = this.getToken();
        const headers = { ...this.headers, ...customHeaders };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        return headers;
    }

    // Generic HTTP request
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: this.buildHeaders(options.headers),
            signal: AbortSignal.timeout(this.timeout)
        };

        try {
            const response = await fetch(url, config);
            
            // Handle unauthorized
            if (response.status === 401) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = '/index.html';
                throw new Error('Sessão expirada. Faça login novamente.');
            }

            // Parse JSON response
            const data = await response.json();

            // Handle error responses
            if (!response.ok) {
                throw new Error(data.error || data.message || 'Erro na requisição');
            }

            return data;

        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Requisição timeout. Tente novamente.');
            }
            throw error;
        }
    }

    // HTTP GET
    async get(endpoint, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        
        return this.request(url, {
            method: 'GET'
        });
    }

    // HTTP POST
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // HTTP PUT
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // HTTP DELETE
    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }
}

// Initialize API client
const api = new APIClient(API_CONFIG);

// API Endpoints
const API = {
    // Authentication
    auth: {
        login: (email, password) => api.post('/auth/login', { email, password }),
        logout: () => api.post('/auth/logout'),
        me: () => api.get('/auth/me')
    },

    // Metrics
    metrics: {
        getAll: (params) => api.get('/metrics', params),
        getById: (id) => api.get(`/metrics/${id}`),
        create: (data) => api.post('/metrics', data),
        update: (id, data) => api.put(`/metrics/${id}`, data),
        delete: (id) => api.delete(`/metrics/${id}`),
        summary: (params) => api.get('/metrics/summary', params)
    },

    // Schedule
    schedule: {
        getAll: (params) => api.get('/schedule', params),
        update: (id, data) => api.put(`/schedule/${id}`, data)
    },

    // Alerts
    alerts: {
        getAll: (params) => api.get('/alerts', params),
        getConfig: () => api.get('/alerts/config'),
        updateConfig: (data) => api.put('/alerts/config', data)
    },

    // Hooks
    hooks: {
        getAll: (params) => api.get('/hooks', params),
        increment: (id) => api.put(`/hooks/${id}/increment`)
    },

    // Config
    config: {
        getAll: () => api.get('/config')
    }
};

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.API = API;
    window.api = api;
}

