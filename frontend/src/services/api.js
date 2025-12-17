import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 60000,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    response => response,
    error => {
        console.error('Error en la solicitud API:', error);
        return Promise.reject(error);
    }
);

export default api;

//para que funcione en produccion