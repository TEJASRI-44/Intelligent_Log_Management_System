// src/pages/admin/AdminDashboard.jsx
import { useState } from "react";
import { getCurrentUser } from "../auth/auth.api";

import AdminLayout from "../components/AdminLayout";
import AdminSidebar from "../components/AdminSidebar";
import AdminHeader from "../components/AdminHeader";

import AdminCreateUser from "./AdminCreateUser";
import AdminReports from "./AdminReports";
import ManageUsers from "./ManageUsers";
import AdminLogSearch from "./AdminLogSearch";
import AdminManageFiles from "./AdminManagefiles";
import AdminSecurity from "./AdminSecurity";
import AdminAudits from "./AdminAudits";
import Profile from "./Profile";

import "../styles/adminDashboard.css";
import "bootstrap/dist/css/bootstrap.min.css";

export default function AdminDashboard() {
  const [activePage, setActivePage] = useState("reports");
  const user = getCurrentUser();

  return (
    <AdminLayout
      sidebar={
        <AdminSidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />
      }
      header={<AdminHeader user={user} />}
    >
      {activePage === "reports" && <AdminReports />}
      {activePage === "create-user" && <AdminCreateUser />}
      {activePage === "manage-users" && <ManageUsers />}
      {activePage === "logs" && <AdminLogSearch />}
      {activePage === "files" && <AdminManageFiles />}
      {activePage === "security" && <AdminSecurity />}
      {activePage === "audits" && <AdminAudits />}
      {activePage === "profile" && <Profile />}
    </AdminLayout>
  );
}
