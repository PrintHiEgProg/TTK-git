// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getClients = async () => {
  try {
    const response = await api.get('/api/clients/');
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении данных о клиентах:', error);
    throw error;
  }
};

export const createClients = async (clientData, config) => {
  try {
    const response = await api.post('/api/clients/create/', clientData, config);
    return response.data;
  } catch (error) {
    console.error('Ошибка при создании клиента:', error);
    throw error;
  }
};

export const deleteClients = async (id, config) => {
  try {
    await api.delete(`/api/clients/delete/${id}/`, config);
  } catch (error) {
    console.error('Ошибка при удалении клиента:', error);
    throw error;
  }
};


export const getIntentions = async () => {
  try {
    const response = await api.get('/api/intents');
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении данных:', error);
    throw error;
  }
};

export const createIntention = async (data, config) => {
  try {
    const response = await api.post('/api/intents/create/', data, config);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Ошибка при создании intention:', error);
    throw error;
  }
};

export const deleteIntention = async (id, config) => {
  try {
    await api.delete(`/api/intents/delete/${id}/`, config);
  } catch (error) {
    console.error('Ошибка при удалении intention:', error);
    throw error;
  }
};

export default api;
