import { useState } from "react";
import api from "../../services/api"; // Обновленный путь к api.js
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../constants"; // Обновленный путь к constants.js
import "../../styles/Login_Form.css"; // Обновленный путь к стилям

function LoginForm() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate(); // Хук для навигации между страницами

    const handleSubmit = async (e) => {
        e.preventDefault(); // Предотвращаем перезагрузку страницы при сабмите формы
        setLoading(true);

        try {
            // Выполнение POST-запроса для логина
            const res = await api.post("/api/token/", { username, password });

            // Сохранение токенов в localStorage
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);

            // Перенаправление на административную панель
            window.location.href = '/panel/';
        } catch (error) {
            alert("Ошибка входа. Проверьте свои учетные данные.");
        } finally {
            setLoading(false); // Останавливаем загрузку в любом случае
        }
    };

    return (
        <div className="form-wrapper">
            <form onSubmit={handleSubmit} className="form-container">
                <h1 className="form-title">Login</h1>
                <div className="form-group">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                        className="form-input"
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Enter your username"
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                        className="form-input"
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        required
                    />
                </div>
                {loading && <div className="loading-text">Loading...</div>}
                <button className="form-button" type="submit" disabled={loading}>
                    {loading ? "Logging in..." : "Login"}
                </button>
            </form>
        </div>
    );
}

export default LoginForm;
