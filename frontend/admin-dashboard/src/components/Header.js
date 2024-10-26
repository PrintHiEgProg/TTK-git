import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/Header.css';

function Header({ toggleSidebar, isSidebarOpen }) {
  const navigate = useNavigate(); // Хук для навигации между страницами

  // Функция для выхода пользователя
  const handleLogout = () => {
    localStorage.clear();
    window.location.href = '/login';
  };

  return (
    <header className="header">
      <div className="burger__panel">
        <div
          id="burger"
          className={`burger ${isSidebarOpen ? 'active' : ''}`}
          onClick={toggleSidebar}
        >
          <span></span>
        </div>
        <h2 className="header-text">Админ-панель</h2>
        <nav className={isSidebarOpen ? 'active' : ''}>
          <h2><Link to="/panel/">Главная</Link></h2>
          <h2><Link to="/panel/users">Пользователи</Link></h2>
          <h2><Link to="/panel/settings">Намерения</Link></h2>
        </nav>
      </div>
      <button className="logout-button" onClick={handleLogout}>
        Выйти
      </button>
    </header>
  );
}

export default Header;
