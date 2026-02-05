// src/components/user/UserSidebar.jsx
import { NavLink } from "react-router-dom";

export default function UserSidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">LogHub Dashboard</div>
      </div>

      <nav className="sidebar-nav">

        <NavLink
          to="/user/logs"
          className={({ isActive }) =>
            `nav-item  text-decoration-none ${isActive ? "active" : "text-decoration-none"}`
          }
        >
          <span className="nav-text">Overview & Logs</span>
        </NavLink>

        <NavLink
          to="/user/upload-file"
          className={({ isActive }) =>
            `nav-item text-decoration-none ${isActive ? "active" : "text-decoration-none"}`
          }
        >
          <span className="nav-text">Upload Files</span>
        </NavLink>

        <NavLink
          to="/user/my-files"
          className={({ isActive }) =>
            `nav-item text-decoration-none ${isActive ? "active" : "text-decoration-none"}`
          }
        >
          <span className="nav-text">My Files</span>
        </NavLink>

        <NavLink
          to="/user/profile"
          className={({ isActive }) =>
            `nav-item text-decoration-none ${isActive ? "active" : "text-decoration-none"}`
          }
        >
          <span className="nav-text">Profile</span>
        </NavLink>

      </nav>
    </aside>
  );
}
