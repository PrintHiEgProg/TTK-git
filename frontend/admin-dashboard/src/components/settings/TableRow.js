import React from 'react';

const TableRow = ({ row, deleteRow }) => {
  return (
    <tr>
      <td>{row.name}</td>
      <td>{row.keywords}</td>
      <td>{row.response_text}</td>
      <td>{row.email}</td>
      <td>
        <button onClick={() => deleteRow(row.id)}>Удалить</button>
      </td>
    </tr>
  );
};

export default TableRow;
