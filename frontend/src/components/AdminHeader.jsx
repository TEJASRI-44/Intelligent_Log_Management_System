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
      <h1 className="mb-0">Admin Dashboard</h1>

      <div className="d-flex align-items-center gap-3">
        <span className="text-muted small">{user?.email}</span>

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
