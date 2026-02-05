// src/pages/admin/AdminDashboard.jsx
import { Outlet } from "react-router-dom";
import { getCurrentUser } from "../auth/auth.api";

import AdminLayout from "../components/AdminLayout";
import AdminSidebar from "../components/AdminSidebar";
import AdminHeader from "../components/AdminHeader";

import "../styles/adminDashboard.css";
import "bootstrap/dist/css/bootstrap.min.css";

export default function AdminDashboard() {
  const user = getCurrentUser();

  return (
    <AdminLayout
      sidebar={<AdminSidebar />}
      header={<AdminHeader user={user} />}
    >
      <Outlet />
    </AdminLayout>
  );
}
