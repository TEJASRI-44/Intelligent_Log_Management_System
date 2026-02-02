// src/pages/admin/components/AdminSidebar.jsx
export default function AdminSidebar({ activePage, setActivePage }) {
  return (
    <aside className="admin-sidebar">
      <h2 className="logo">ILMS Admin</h2>

      <nav>
        {[
          ["reports", "Reports"],
          ["create-user", "Create User"],
          ["manage-users", "Manage Users"],
          ["logs", "Logs"],
          ["files", "Files"],
          ["security", "Security"],
          ["audits", "Audits"],
          ["profile", "Profile"]
        ].map(([key, label]) => (
          <button
            key={key}
            className={activePage === key ? "active" : ""}
            onClick={() => setActivePage(key)}
          >
            {label}
          </button>
        ))}
      </nav>
    </aside>
  );
}
