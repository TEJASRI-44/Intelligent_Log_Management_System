// src/pages/admin/components/AdminLayout.jsx
export default function AdminLayout({ sidebar, header, children }) {
  return (
    <div className="admin-layout">
      {sidebar}

      <main className="main-admindashboard-content">
        {header}
        <section className="page-admindashboard-content">
          {children}
        </section>
      </main>
    </div>
  );
}
