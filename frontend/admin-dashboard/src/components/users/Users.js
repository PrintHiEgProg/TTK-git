// src/components/settings/Settings.js
import React, { useState, useEffect } from 'react';
import '../../styles/Users.css';
import Table from './Table';
import './styles.css';
import { getClients, createClients, deleteClients } from '../../services/api';

const Clients = () => {
  const [isAdmin, setIsAdmin] = useState(true);
  const [data, setData] = useState([]);
  const [newRow, setNewRow] = useState({ contract_number: '', contact_phone: '', address: ''});
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    // Функция для получения данных о клиентах из API
    const fetchData = async () => {
      try {
        const clients = await getClients();
        setData(clients);
      } catch (err) {
        console.error('Ошибка при загрузке данных:', err);
        setError('Ошибка при загрузке данных клиентов.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const addRow = async () => {
    try {
      setError(null);
      setIsAdding(true);

      // Проверка на дублирующиеся записи
      const isDuplicate = data.some(
        (row) => row.contract_number === newRow.contract_number && row.contact_phone === newRow.contact_phone
      );

      // Получаем токен JWT из localStorage
      const token = localStorage.getItem('access');

      // Конфигурируем запрос с использованием JWT токена
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      if (isDuplicate) {
        console.warn('Этот клиент уже существует. Невозможно добавить дублирующиеся записи.');
        setError('Этот клиент уже существует.');
        return;
      }

      // Добавление нового клиента через API
      const newClient = await createClients(newRow, config);

      // Обновляем состояние с новыми данными
      setData([...data, newClient]);
      setNewRow({ contract_number: '', contact_phone: '', address: ''});
    } catch (error) {
      console.error('Ошибка при добавлении нового клиента:', error);
      setError('Не удалось добавить клиента. Пожалуйста, попробуйте снова.');
    } finally {
      setIsAdding(false);
    }
  };

  const deleteRow = async (id) => {
    try {
      // Получаем токен JWT из localStorage
      const token = localStorage.getItem('access');

      // Конфигурируем запрос с использованием JWT токена
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      await deleteClients(id, config);

      // Удаляем строку из состояния
      setData(data.filter((row) => row.id !== id));
    } catch (error) {
      console.error('Ошибка при удалении клиента:', error);
      setError('Не удалось удалить клиента. Пожалуйста, попробуйте снова.');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewRow({ ...newRow, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addRow();
  };

  if (loading) return <p>Загрузка данных...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="main">
      {isAdmin && (
        <div className="settings">
          <h2>Список клиентов</h2>
          <div className="tabl">
            <Table data={data} deleteRow={deleteRow} />
          </div>
          <form onSubmit={handleSubmit} className="add-row-form">
            <h2>Добавить нового клиента</h2>
            <input
              name="contract_number"
              value={newRow.contract_number}
              onChange={handleInputChange}
              placeholder="Номер контракта"
              required
            />
            <input
              name="contact_phone"
              value={newRow.contact_phone}
              onChange={handleInputChange}
              placeholder="Номер телефона"
              required
            />
            <input
              name="address"
              value={newRow.passwd}
              onChange={handleInputChange}
              placeholder="Адрес"
              required
            />
            <button type="submit" disabled={isAdding}>
              {isAdding ? 'Добавление...' : 'Добавить'}
            </button>
            {error && <p className="error-message">{error}</p>}
          </form>
        </div>
      )}
    </div>
  );
};

export default Clients;
