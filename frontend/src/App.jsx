import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import AdminDashboard from "./pages/AdminDashboard";
import UserDashboard from "./pages/UserDashboard";
import ProtectedRoute from "./pages/ProtectedRoute";
import { isAuthenticated, getRole } from "./auth/auth.service";

import UserSearchLogs from "./pages/UserSearchLogs";
import UserMyFiles from "./pages/UserMyFiles";
import UserUploadFiles from "./pages/UserUploadFiles";
import Profile from "./pages/Profile";
import AdminReports from "./pages/AdminReports";
import AdminCreateUser from "./pages/AdminCreateUser";
import ManageUsers from "./pages/ManageUsers";
import AdminLogSearch from "./pages/AdminLogSearch";
import AdminManageFiles from "./pages/AdminManagefiles";
import AdminSecurity from "./pages/AdminSecurity";
import AdminAudits from "./pages/AdminAudits";
import { ToastContainer } from "react-toastify";

export default function App() {
  return (
    
    <>
      <Routes>

      <Route path="/" element={<Home />} />

      <Route
        path="/login"
        element={
          isAuthenticated()
            ? getRole() === "ADMIN"
              ? <Navigate to="/admin" />
              : <Navigate to="/user" />
            : <Login />
        }
      />

      <Route
        path="/user"
        element={
          <ProtectedRoute allowedRoles={["USER"]}>
            <UserDashboard />
          </ProtectedRoute>
        }
      >
        <Route index element={<UserSearchLogs />} />
        <Route path="logs" element={<UserSearchLogs />} />
        <Route path="upload-file" element={<UserUploadFiles />} />
        <Route path="my-files" element={<UserMyFiles />} />
        <Route path="profile" element={<Profile />} />
      </Route>
   

      <Route
        path="/admin"
        element={
          <ProtectedRoute allowedRoles={["ADMIN"]}>
            <AdminDashboard />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="reports" />} />
        <Route path="reports" element={<AdminReports />} />
        <Route path="create-user" element={<AdminCreateUser />} />
        <Route path="manage-users" element={<ManageUsers />} />
        <Route path="logs" element={<AdminLogSearch />} />
        <Route path="files" element={<AdminManageFiles />} />
        <Route path="security" element={<AdminSecurity />} />
        <Route path="audits" element={<AdminAudits />} />
        <Route path="profile" element={<Profile />} />
      </Route>

      <Route path="*" element={<Navigate to="/" />} />

    </Routes>
    <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        pauseOnHover
        draggable
        theme="dark"
      />
    </>
   
  );
}
