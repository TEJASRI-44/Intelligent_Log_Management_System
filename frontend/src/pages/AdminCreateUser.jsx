import { useEffect, useState } from "react";
import { createUser, fetchRoles, fetchTeams } from "../api/admin.api";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/AdminCreateUserScoped.css";

export default function AdminCreateUser() {
  const [roles, setRoles] = useState([]);
  const [teams, setTeams] = useState([]);

  const [form, setForm] = useState({
    email: "",
    username: "",
    password: "",
    first_name: "",
    last_name: "",
    job_title: "",
    role_ids: [],
    team_ids: []
  });

  useEffect(() => {
    fetchRoles().then(setRoles);
    fetchTeams().then(setTeams);
  }, []);

  const handleMultiSelect = (e, key) => {
    const values = Array.from(e.target.selectedOptions).map(o => Number(o.value));
    setForm({ ...form, [key]: values });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createUser(form);
    alert("User created successfully");
  };

  return (
    <div className="acu-root container-fluid py-4">
      <div className="acu-wrapper mx-auto">

        <div className="card shadow-sm acu-card">
          <div className="card-header acu-header">
            <h4 className="mb-1">Create New User</h4>
            <small className="text-muted">
              Create account and assign access permissions
            </small>
          </div>

          <div className="card-body">
            <form onSubmit={handleSubmit}>

              {/* ACCOUNT */}
              <div className="acu-section">
                <h6 className="acu-section-title">Account Details</h6>
                <div className="row g-3">
                  <div className="col-md-4">
                    <label className="form-label">Email *</label>
                    <input
                      className="form-control"
                      required
                      onChange={e => setForm({ ...form, email: e.target.value })}
                    />
                  </div>

                  <div className="col-md-4">
                    <label className="form-label">Username</label>
                    <input
                      className="form-control"
                      onChange={e => setForm({ ...form, username: e.target.value })}
                    />
                  </div>

                  <div className="col-md-4">
                    <label className="form-label">Password *</label>
                    <input
                      type="password"
                      className="form-control"
                      required
                      onChange={e => setForm({ ...form, password: e.target.value })}
                    />
                  </div>
                </div>
              </div>

              {/* PROFILE */}
              <div className="acu-section">
                <h6 className="acu-section-title">Profile Information</h6>
                <div className="row g-3">
                  <div className="col-md-4">
                    <label className="form-label">First Name *</label>
                    <input
                      className="form-control"
                      required
                      onChange={e => setForm({ ...form, first_name: e.target.value })}
                    />
                  </div>

                  <div className="col-md-4">
                    <label className="form-label">Last Name</label>
                    <input
                      className="form-control"
                      onChange={e => setForm({ ...form, last_name: e.target.value })}
                    />
                  </div>

                  <div className="col-md-4">
                    <label className="form-label">Job Title</label>
                    <input
                      className="form-control"
                      onChange={e => setForm({ ...form, job_title: e.target.value })}
                    />
                  </div>
                </div>
              </div>

              {/* ACCESS */}
              <div className="acu-section">
                <h6 className="acu-section-title">Access Control</h6>
                <div className="row g-4">
                  <div className="col-md-6">
                    <label className="form-label">Roles</label>
                    <select
                      multiple
                      size="6"
                      className="form-select"
                      onChange={e => handleMultiSelect(e, "role_ids")}
                    >
                      {roles.map(r => (
                        <option key={r.role_id} value={r.role_id}>
                          {r.role_name}
                        </option>
                      ))}
                    </select>
                    <small className="text-muted">
                      Hold Ctrl / Cmd to select multiple
                    </small>
                  </div>

                  <div className="col-md-6">
                    <label className="form-label">Teams</label>
                    <select
                      multiple
                      size="6"
                      className="form-select"
                      onChange={e => handleMultiSelect(e, "team_ids")}
                    >
                      {teams.map(t => (
                        <option key={t.team_id} value={t.team_id}>
                          {t.team_name}
                        </option>
                      ))}
                    </select>
                    <small className="text-muted">
                      Hold Ctrl / Cmd to select multiple
                    </small>
                  </div>
                </div>
              </div>

              {/* ACTION */}
              <div className="d-flex justify-content-end pt-3">
                <button className="btn btn-primary px-4">
                  Create User
                </button>
              </div>

            </form>
          </div>
        </div>

      </div>
    </div>
  );
}
