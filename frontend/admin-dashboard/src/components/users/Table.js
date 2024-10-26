import React from 'react';
import TableRow from './TableRow';

const Table = ({ data, deleteRow, updateRow }) => {
  return (
    <table className="table">
      <thead>
        <tr>
          <th>Номер контракта</th>
          <th>Номер телефона</th>
          <th>Адрес</th>
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