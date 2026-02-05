import { useEffect } from "react";
import { useNavigate, Outlet } from "react-router-dom";
import UserSidebar from "../components/UserSidebar";
import "../styles/UserDashboard.css";

export default function UserDashboard() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login", { replace: true });
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/login", { replace: true });
  };

  return (
    <div className="dashboard-layout">
      {/* SIDEBAR */}
      <UserSidebar />

      {/* MAIN AREA */}
      <div className="dashboard-main">
        <header className="dashboard-header">
          <h1>Intelligent Log Management System</h1>
          <button className="logout-btn" onClick={handleLogout}>
            Sign Out
          </button>
        </header>

        {/* ROUTED CONTENT */}
        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
