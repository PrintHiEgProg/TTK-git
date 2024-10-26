// src/components/settings/Settings.js
import React, { useState, useEffect } from 'react';
import '../../styles/Settings.css';
import Table from './Table';
import './styles.css';
import { getIntentions, createIntention, deleteIntention } from '../../services/api';

const Settings = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newRow, setNewRow] = useState({ name: '', keywords: '', response_text: '', email: '' });
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const intentions = await getIntentions();
        setData(intentions);
      } catch (err) {
        setError('Ошибка при загрузке данных');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const addRow = async () => {
    const isDuplicate = data.some(
      (row) => row.name === newRow.name && row.keywords === newRow.keywords
    );

    if (isDuplicate) {
      console.warn('Эта строка уже существует. Невозможно добавить дублирующиеся строки.');
      setError('Эта строка уже существует.');
      return;
    }

    try {
      setError(null);
      setIsAdding(true);

      // Получаем токен JWT из localStorage
      const token = localStorage.getItem('access');

      // Конфигурируем запрос с использованием JWT токена
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      // Отправляем запрос на добавление новой строки
      const response = await createIntention(newRow, config);

      // Обновляем состояние с новыми данными
      setData((prevData) => [...prevData, response]);
      setNewRow({ name: '', keywords: '', response_text: '', email: '' });
    } catch (error) {
      console.error('Ошибка при добавлении новой строки:', error);
      setError('Не удалось добавить строку. Пожалуйста, попробуйте снова.');
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

      await deleteIntention(id, config);

      // Удаляем строку из состояния
      setData((prevData) => prevData.filter((row) => row.id !== id));
    } catch (error) {
      console.error('Ошибка при удалении строки:', error);
      setError('Не удалось удалить строку. Пожалуйста, попробуйте снова!!.');
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
      <div className="settings">
        <h2>Список намерений</h2>
        <div className="tabl">
          <Table data={data} deleteRow={deleteRow} />
        </div>
        <form onSubmit={handleSubmit} className="add-row-form">
          <h2>Добавить новую строку</h2>
          <input
            name="name"
            value={newRow.name}
            onChange={handleInputChange}
            placeholder="Намерение"
            required
          />
          <input
            name="keywords"
            value={newRow.keywords}
            onChange={handleInputChange}
            placeholder="Ключевые слова"
            required
          />
          <input
            name="response_text"
            value={newRow.response_text}
            onChange={handleInputChange}
            placeholder="Сопроводительный текст"
            required
          />
          <input
            name="email"
            value={newRow.email}
            onChange={handleInputChange}
            placeholder="Email"
            required
          />
          <button type="submit" disabled={isAdding}>
            {isAdding ? 'Добавление...' : 'Добавить'}
          </button>
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
};

export default Settings;
