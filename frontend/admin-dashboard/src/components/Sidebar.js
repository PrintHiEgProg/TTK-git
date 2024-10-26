import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Sidebar.css';

function Sidebar({ isSidebarOpen, toggleSidebar }) {
  const [isAdmin, setIsAdmin] = useState(true);

  return (
    <aside id="sidebar" className={`sidebar ${isSidebarOpen ? 'sactive' : ''}`}>
      <ul>
        <li><h2><Link to="/panel/" onClick={toggleSidebar}>Главная</Link></h2></li>
        {isAdmin && (<li><h2><Link to="/panel/users" onClick={toggleSidebar}>Пользователи</Link></h2></li>)}
        <li><h2><Link to="/panel/settings" onClick={toggleSidebar}>Намерения</Link></h2></li>
      </ul>
    </aside>
  );
}

export default Sidebar;