import React from 'react';
import TableRow from './TableRow';

const Table = ({ data, deleteRow, updateRow }) => {
  return (
    <table className="table">
      <thead>
        <tr>
          <th>Намерение</th>
          <th>Ключевые слова</th>
          <th>Сопроводительный текст</th>
          <th>Email</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <TableRow key={row.id} row={row} deleteRow={deleteRow} updateRow={updateRow} />
        ))}
      </tbody>
    </table>
  );
};

export default Table;