import React from 'react';

const TableRow = ({ row, deleteRow }) => {
  return (
    <tr>
      <td>{row.contract_number}</td>
      <td>{row.contact_phone}</td>
      <td>{row.address}</td>
      <td>
        <button onClick={() => deleteRow(row.id)}>Удалить</button>
      </td>
    </tr>
  );
};

export default TableRow;
