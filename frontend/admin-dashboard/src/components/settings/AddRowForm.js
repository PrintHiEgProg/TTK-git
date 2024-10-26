import React, { useState } from 'react';

const AddRowForm = ({ addRow }) => {
  const [newRow, setNewRow] = useState({ name: '', keywords: '', response_text: '', email: '' });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewRow({ ...newRow, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addRow(newRow);
    setNewRow({ name: '', keywords: '', response_text: '', email: '' });
  };

  return (
    <form onSubmit={handleSubmit} className="add-row-form">
      <h2>Добавить новую строку</h2>
      <input name="name" value={newRow.name} onChange={handleInputChange} placeholder="Намерение" required />
      <input name="keywords" value={newRow.keywords} onChange={handleInputChange} placeholder="Ключевые слова" required />
      <input name="response_text" value={newRow.response_text} onChange={handleInputChange} placeholder="Сопроводительный текст" required />
      <input name="email" value={newRow.email} onChange={handleInputChange} placeholder="Email" required />
      <button type="submit">Добавить</button>
    </form>
  );
};

export default AddRowForm;