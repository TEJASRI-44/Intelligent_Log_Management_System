import { NavLink } from "react-router-dom";

export default function AdminSidebar() {
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

  return (
    <aside className="admin-sidebar">
      <h2 className="logo">ILMS Admin</h2>

      <nav>
        {links.map(([path, label]) => (
          <NavLink
            key={path}
            to={`/admin/${path}`}
            className={({ isActive }) =>
              `nav-item text-decoration-none ${isActive ? "active" : "text-decoration-none"}`
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
