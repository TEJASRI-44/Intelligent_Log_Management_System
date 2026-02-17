import { useEffect, useState } from "react";
import { updateUserProfile, updateUserAccess } from "../api/adminUsers.api";
import { fetchRoles, fetchTeams } from "../api/admin.api";
import "../styles/EditUserModal.css";
import { toast } from "react-toastify";

export default function EditUserModal({ user, onClose, onSaved }) {
  const [roles, setRoles] = useState([]);
  const [teams, setTeams] = useState([]);
  const [originalProfile, setOriginalProfile] = useState({});
  
  const [selectedRoles, setSelectedRoles] = useState([]);
  const [selectedTeams, setSelectedTeams] = useState([]);
  const [saving, setSaving] = useState(false);
 const [profile, setProfile] = useState({
    first_name: "",
    last_name: "",
    phone_number: "",
    job_title: ""
  });
  useEffect(() => {
  console.log("EDIT USER OBJECT:", user);
}, [user]);

  /* ===== LOAD INITIAL VALUES ===== */
 useEffect(() => {
  const p = user.profile || {};

  setOriginalProfile(p);
  setProfile({
    first_name: p.first_name || "",
    last_name: p.last_name || "",
    phone_number: p.phone_number || "",
    job_title: p.job_title || ""
  });

  setSelectedRoles(user.role_ids || []);
  setSelectedTeams(user.team_ids || []);

  fetchRoles().then(setRoles);
  fetchTeams().then(setTeams);
}, [user]);


  function toggle(id, list, setList) {
    setList(
      list.includes(id) ? list.filter((x) => x !== id) : [...list, id]
    );
  }



async function save() {
  try {
    setSaving(true);

    const payload = {};

    if (profile.first_name !== undefined)
      payload.first_name = profile.first_name;

    if (profile.last_name !== undefined)
      payload.last_name = profile.last_name;

    if (profile.phone_number !== undefined)
      payload.phone_number = profile.phone_number;

    if (profile.job_title !== undefined)
      payload.job_title = profile.job_title;

    await Promise.all([
      Object.keys(payload).length > 0 &&
        updateUserProfile(user.user_id, payload),
      updateUserAccess(user.user_id, selectedRoles, selectedTeams),
    ]);

    toast.success("User updated successfully ");

    onSaved();
  } catch (error) {
    console.error(error);
    toast.error("Failed to update user ");
  } finally {
    setSaving(false);
  }
}


  return (
    <div className="custom-modal-backdrop show" onClick={onClose}>
      <div className="modal-dialog modal-dialog-centered modal-lg">
        <div
          className="modal-content shadow-lg"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="modal-header border-bottom">
            <div>
              <h5 className="modal-title mb-1">Edit User</h5>
              <p className="text-muted small mb-0">{user.email}</p>
            </div>
            <button
              type="button"
              className="btn-close"
              onClick={onClose}
              aria-label="Close"
            ></button>
          </div>

          {/* Body */}
          <div className="modal-body">
            {/* Profile Information Section */}
            <div className="mb-4">
              <h6 className="text-uppercase text-muted small fw-semibold mb-3">
                Profile Information
              </h6>
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label small text-muted">
                    First Name
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    value={profile.first_name}
                    onChange={(e) =>
                      setProfile({ ...profile, first_name: e.target.value })
                    }
                  />

                </div>
                <div className="col-md-6">
                  <label className="form-label small text-muted">
                    Last Name
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder={originalProfile.last_name || "Enter last name"}
                    value={profile.last_name || ""}
                    onChange={(e) =>
                      setProfile({ ...profile, last_name: e.target.value })
                    }
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label small text-muted">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    className="form-control"
                    placeholder={originalProfile.phone_number || "Enter phone number"}
                    value={profile.phone_number || ""}
                    onChange={(e) =>
                      setProfile({ ...profile, phone_number: e.target.value })
                    }
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label small text-muted">
                    Job Title
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder={originalProfile.job_title || "Enter job title"}
                    value={profile.job_title || ""}
                    onChange={(e) =>
                      setProfile({ ...profile, job_title: e.target.value })
                    }
                  />
                </div>
              </div>
            </div>

            {/* Roles Section */}
            <div className="mb-4">
              <h6 className="text-uppercase text-muted small fw-semibold mb-3">
                Roles
              </h6>
              <div className="role-team-grid">
                {roles.map((r) => (
                  <div key={r.role_id} className="form-check">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      id={`role-${r.role_id}`}
                      checked={selectedRoles.includes(r.role_id)}
                      onChange={() =>
                        toggle(r.role_id, selectedRoles, setSelectedRoles)
                      }
                    />
                    <label
                      className="form-check-label"
                      htmlFor={`role-${r.role_id}`}
                    >
                      {r.role_name}
                    </label>
                  </div>
                ))}
              </div>
            </div>

            {/* Teams Section */}
            <div className="mb-3">
              <h6 className="text-uppercase text-muted small fw-semibold mb-3">
                Teams
              </h6>
              <div className="role-team-grid">
                {teams.map((t) => (
                  <div key={t.team_id} className="form-check">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      id={`team-${t.team_id}`}
                      checked={selectedTeams.includes(t.team_id)}
                      onChange={() =>
                        toggle(t.team_id, selectedTeams, setSelectedTeams)
                      }
                    />
                    <label
                      className="form-check-label"
                      htmlFor={`team-${t.team_id}`}
                    >
                      {t.team_name}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="modal-footer border-top bg-light">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              disabled={saving}
            >
              Cancel
            </button>
            <button
              type="button"
              className="btn btn-primary"
              onClick={save}
              disabled={saving}
            >
              {saving ? (
                <>
                  <span
                    className="spinner-border spinner-border-sm me-2"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  Saving...
                </>
              ) : (
                "Save Changes"
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}