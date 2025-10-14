import api from './api';

export const getExpedientes = async () => {
    try {
        const response = await api.get('/expedientes/');
        return response.data;
    } catch (error) {
        console.error('Error extrayendo los expendientes:', error);
        throw error;
    }
}

export const getExpedienteById = async (id) => {
    try {
        const response = await api.get(`/expedientes/${id}/`);
        return response.data;
    } catch (error) {
        console.error(`Error extrayendo el expediente con ID ${id}:`, error);
    }
}