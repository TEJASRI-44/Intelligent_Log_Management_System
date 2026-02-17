import { useState } from "react";
import { NavLink } from "react-router-dom";
import "../styles/AdminSidebar.css";

export default function AdminSidebar() {
  const [isOpen, setIsOpen] = useState(false);

  const links = [
    ["reports", "Reports"],
    ["create-user", "Create User"],
    ["manage-users", "Manage Users"],
    ["logs", "Logs"],
    ["files", "Files"],
    ["security", "Security"],
    ["audits", "Audits"],
    ["profile", "Profile"]
  ];

  const closeSidebar = () => setIsOpen(false);

  return (
    <>
      {/* Mobile Toggle Button */}
      <button
        className="btn  d-md-none mobile-toggle-btn w-10"
        onClick={() => setIsOpen(!isOpen)}
        
      >
        {isOpen ?  <i class="bi text-white bi-x-lg"></i>:<i class="bi bi-list"></i> }
      </button>

      {/* Mobile Overlay */}
      {isOpen && (
        <div className="sidebar-overlay d-md-none" onClick={closeSidebar}></div>
      )}

      <aside className={`admin-sidebar bg-dark ${isOpen ? "open" : ""}`}>
        <div className="sidebar-brand mt-0">
          <h2 className="logo text-white fs-4 mb-0">ILMS Admin</h2>
        </div>

        <nav className="sidebar-nav nav nav-pills flex-column gap-1 px-3">
          {links.map(([path, label]) => (
            <NavLink
              key={path}
              to={`/admin/${path}`}
              onClick={closeSidebar}
              className={({ isActive }) =>
                `nav-link ${isActive ? "active bg-primary" : "text-white link-hover"}`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
    </>
  );
}