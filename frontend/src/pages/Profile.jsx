import { useEffect, useState } from "react";
import { fetchMyProfile, updateMyProfile } from "../api/user.api";
import { useNavigate } from "react-router-dom";
import {toast} from "react-toastify"
import ChangePasswordModal from "./ChangePasswordModal";


import "../styles/Profile.css";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    phone_number: ""
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [showChangePassword, setShowChangePassword] = useState(false);

  const navigate = useNavigate();

 

  useEffect(() => {
    loadProfile();
  }, []);

  async function loadProfile() {
    try {
      const data = await fetchMyProfile();
      setProfile(data);
      setForm({
        first_name: data.first_name || "",
        last_name: data.last_name || "",
        phone_number: data.phone_number || ""
      });
    } catch {
      alert("Failed to load profile");
    } finally {
      setLoading(false);
    }
  }


  async function handleSave() {
    setSaving(true);
    try {
      await updateMyProfile(form);
      toast.success("Profile Updated Successfully")
      await loadProfile();
      setEditMode(false);
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update profile");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <p>Loading profile...</p>;
  if (!profile) return <p>No profile data available</p>;

  return (
    <div className="container-fluid px-4 py-4 user-profile-page">

      {/* HEADER */}
      <div className="user-profile-header">
        <h2>My Profile</h2>
        <p>View and manage your personal information</p>
      </div>

      {/* CARD */}
      <div className="card shadow-sm user-profile-card">

        {/* CARD HEADER */}
        <div className="card-header d-flex justify-content-between align-items-center">
          <h5 className="mb-0">Account Details</h5>

          {!editMode ? (
            <button
              className="btn btn-sm btn-outline-primary user-profile-edit-btn"
              onClick={() => setEditMode(true)}
            >
              Edit Profile
            </button>
          ) : (
            <div className="user-profile-actions">
              <button
                className="btn btn-sm btn-secondary user-profile-cancel-btn"
                onClick={() => {
                  setEditMode(false);
                  setForm({
                    first_name: profile.first_name || "",
                    last_name: profile.last_name || "",
                    phone_number: profile.phone_number || ""
                  });
                }}
              >
                Cancel
              </button>

              <button
                className="btn btn-sm btn-primary user-profile-save-btn"
                onClick={handleSave}
                disabled={saving}
              >
                {saving ? "Saving..." : "Save"}
              </button>
            </div>
          )}
        </div>

        {/* CARD BODY */}
        <div className="card-body">
          <div className="row g-3">

            {/* EMAIL */}
            <div className="col-md-6">
              <label>Email</label>
              <input
                className="form-control"
                value={profile.email}
                disabled
              />
            </div>

            {/* USERNAME */}
            <div className="col-md-6">
              <label>Username</label>
              <input
                className="form-control"
                value={profile.username || "-"}
                disabled
              />
            </div>

            {/* FIRST NAME */}
            <div className="col-md-4">
              <label>First Name</label>
              <input
                className="form-control"
                value={form.first_name}
                disabled={!editMode}
                onChange={e =>
                  setForm({ ...form, first_name: e.target.value })
                }
              />
            </div>

            {/* LAST NAME */}
            <div className="col-md-4">
              <label>Last Name</label>
              <input
                className="form-control"
                value={form.last_name}
                disabled={!editMode}
                onChange={e =>
                  setForm({ ...form, last_name: e.target.value })
                }
              />
            </div>

            {/* PHONE */}
            <div className="col-md-4">
              <label>Phone Number</label>
              <input
                className="form-control"
                value={form.phone_number}
                disabled={!editMode}
                onChange={e =>
                  setForm({ ...form, phone_number: e.target.value })
                }
              />
            </div>

            {/* JOB TITLE */}
            <div className="col-md-6">
              <label>Job Title</label>
              <input
                className="form-control"
                value={profile.job_title || "-"}
                disabled
              />
            </div>

            {/* STATUS */}
            <div className="col-md-6">
              <label>Status</label>
              <input
                className="form-control"
                value={profile.is_active ? "Active" : "Inactive"}
                disabled
              />
            </div>

            {/* CREATED */}
            <div className="col-md-6">
              <label>Account Created</label>
              <input
                className="form-control"
                value={new Date(profile.created_at).toLocaleString()}
                disabled
              />
            </div>
            <div className="card mt-4">
  <div className="card-body">
    <h5 className="mb-2">Security</h5>
    <p className="text-muted">
      Update your password to keep your account secure.
    </p>

    <button
      className="btn btn-outline-primary"
      onClick={() => setShowChangePassword(true)}
    >
      Change Password
    </button>
  </div>
</div>
<ChangePasswordModal
  show={showChangePassword}
  onClose={() => setShowChangePassword(false)}
/>



          </div>
        </div>
      </div>
    </div>
  );
}
