import { useEffect, useState } from "react";
import { createUser, fetchRoles, fetchTeams } from "../api/admin.api";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/AdminCreateUserScoped.css";
import { toast } from "react-toastify";
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

  const handleCheckboxChange = (e, field) => {
  const value = parseInt(e.target.value);

  setForm(prev => {
    const currentValues = prev[field] || [];

    if (e.target.checked) {
      return {
        ...prev,
        [field]: [...currentValues, value]
      };
    } else {
      return {
        ...prev,
        [field]: currentValues.filter(id => id !== value)
      };
    }
  });
};


const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    await createUser(form);

    toast.success("User Created Successfully!");
    setForm({
      name: "",
      email: "",
      password: "",
      role_ids: [],
      team_ids: []
    });

  } catch (error) {
    toast.error("Something went wrong");
  }
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
                      value={form.email}
                      required
                      onChange={e => setForm({ ...form, email: e.target.value })}
                    />
                  </div>

                  <div className="col-md-4">
                    <label className="form-label">Username</label>
                    <input
                    value={form.username}
                      className="form-control"
                      onChange={e => setForm({ ...form, username: e.target.value })}
                    />
                  </div>

                  <div className="col-md-4">
                    <label className="form-label">Password *</label>
                    <input
                      type="password"
                      value={form.password}
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
                      value={form.first_name}
                      required
                      onChange={e => setForm({ ...form, first_name: e.target.value })}
                    />
                  </div>

                  <div className="col-md-4">
                    <label className="form-label">Last Name</label>
                    <input
                      className="form-control"
                      value={form.last_name}
                      onChange={e => setForm({ ...form, last_name: e.target.value })}
                    />
                  </div>

                  <div className="col-md-4">
                    <label className="form-label">Job Title</label>
                    <input
                      className="form-control"
                      value={form.job_title}
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
                  <label className="form-label fw-semibold">Roles</label>

                  <div className="checkbox-container">
                    {roles.map(r => (
                      <div key={r.role_id} className="form-check">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id={`role-${r.role_id}`}
                          value={r.role_id}
                          onChange={(e) => handleCheckboxChange(e, "role_ids")}
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
                <div className="col-md-6">
                  <label className="form-label fw-semibold">Teams</label>

                  <div className="checkbox-container">
                    {teams.map(t => (
                      <div key={t.team_id} className="form-check">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id={`team-${t.team_id}`}
                          value={t.team_id}
                          onChange={(e) => handleCheckboxChange(e, "team_ids")}
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
