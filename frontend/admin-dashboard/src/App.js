import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import NotFound from './components/NotFound';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import Users from './components/users/Users';
import Settings from './components/settings/Settings';
import LoginForm from './components/settings/LoginForm';
import './styles/global.css';

function App() {
  const [isAuth, setIsAuth] = useState(Boolean(localStorage.getItem('access')));

  useEffect(() => {
    const handleStorageChange = () => {
      setIsAuth(Boolean(localStorage.getItem('access')));
    };

    // Listen for localStorage changes (like login setting token)
    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const headerRef = useRef(null);
  const sidebarRef = useRef(null);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleClickOutside = (event) => {
    if (
      headerRef.current &&
      !headerRef.current.contains(event.target) &&
      sidebarRef.current &&
      !sidebarRef.current.contains(event.target)
    ) {
      setIsSidebarOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <Router>
      <div className="app">
        {isAuth && <Header
          toggleSidebar={toggleSidebar}
          isSidebarOpen={isSidebarOpen}
          ref={headerRef}
        />}
        <div className="content">
          {isAuth && <Sidebar isSidebarOpen={isSidebarOpen} toggleSidebar={toggleSidebar} ref={sidebarRef} />}
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login/" element={<LoginForm />} />
            <Route path="*" element={<NotFound />} />
            <Route path="/panel/" element={<Dashboard />} />
            <Route path="/panel/users" element={<Users />} />
            <Route path="/panel/settings" element={<Settings />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;