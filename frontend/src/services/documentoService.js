import api from './api';

export const getDocumentosByExpedienteId = async (expedienteId) => {
    try {
        const response = await api.get(`/documentos/expediente/${expedienteId}/`);
        return response.data;
    } catch (error) {
        console.error(`Error extrayendo los documentos del expediente con ID ${expedienteId}:`, error);
        throw error;
    }
}

export const uploadDocumento = async (formData) => {
    try {
        const response = await api.post('/documentos/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error subiendo el documento:', error);
        throw error;
    }
}