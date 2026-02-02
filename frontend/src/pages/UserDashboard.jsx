import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import UserSidebar from "../components/UserSidebar";

import UserSearchLogs from "./UserSearchLogs";
import UserUploadFiles from "./UserUploadFiles";
import UserMyFiles from "./UserMyFiles";
import Profile from "./Profile";

import "../styles/UserDashboard.css";

export default function UserDashboard() {
  const [activePage, setActivePage] = useState("search");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/", { replace: true });
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/", { replace: true });
  };

  return (
    <div className="dashboard-layout">
      {/* SIDEBAR */}
      <UserSidebar activePage={activePage} setActivePage={setActivePage} />

      {/* MAIN AREA */}
      <div className="dashboard-main">
        {/* HEADER */}
        <header className="dashboard-header">
          <h1>Intelligent Log Management System</h1>
          <button className="logout-btn" onClick={handleLogout}>
            Sign Out
          </button>
        </header>

        {/* PAGE CONTENT */}
        <main className="main-content">
          {activePage === "search" && <UserSearchLogs />}
          {activePage === "upload" && <UserUploadFiles />}
          {activePage === "files" && <UserMyFiles />}
          {activePage === "profile" && <Profile />}
        </main>
      </div>
    </div>
  );
}
