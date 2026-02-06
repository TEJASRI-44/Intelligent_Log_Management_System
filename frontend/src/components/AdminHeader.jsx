// src/pages/admin/components/AdminHeader.jsx
import { useNavigate } from "react-router-dom";
import { logout } from "../auth/auth.api";

export default function AdminHeader({ user }) {
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <header className="header d-flex justify-content-between align-items-center">
      <h2 className=" mb-0">Intelligent Log Management System</h2>

      <div className="d-flex align-items-center gap-3">
        <span className="text-muted small">{user?.username}</span>

        <button
          className="btn btn-outline-danger btn-sm"
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>
    </header>
  );
}
