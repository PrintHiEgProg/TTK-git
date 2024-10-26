import React, { useState } from 'react';

const AddRowForm = ({ addRow }) => {
  const [newRow, setNewRow] = useState({ login: '', passwd: '', role: '', email: '' });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewRow({ ...newRow, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addRow(newRow);
    setNewRow({ login: '', passwd: '', role: '', email: '' });
  };

  return (
    <form onSubmit={handleSubmit} className="add-row-form">
      <h2>Добавить новую строку</h2>
      <input name="login" value={newRow.login} onChange={handleInputChange} placeholder="Логин" required />
      <input name="passwd" value={newRow.passwd} onChange={handleInputChange} placeholder="Пароль" required />
      <input name="role" value={newRow.role} onChange={handleInputChange} placeholder="Роль" required />
      <input name="email" value={newRow.email} onChange={handleInputChange} placeholder="Эл. адрес" required />
      <button type="submit">Добавить</button>
    </form>
  );
};

export default AddRowForm;