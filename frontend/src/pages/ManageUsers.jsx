import { useEffect, useState } from "react";
import {
  fetchUsers,
  updateUserStatus,
  deleteUser
} from "../api/adminUsers.api";
import { getCurrentUserId } from "../auth/auth.api";
import { fetchTeams } from "../api/admin.api";


import EditUserModal from "./EditUserModal";
import "../styles/ManageUsers.css";

export default function ManageUsers() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [error, setError] = useState("");
  const [teams, setTeams] = useState([]);

  const currentUserId = getCurrentUserId();
  
  const [email, setEmail] = useState("");
  const [teamId, setTeamId] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [total, setTotal] = useState(0);


  function onEdit(user) {
    setSelectedUser(user);
  }

  function closeModal() {
    setSelectedUser(null);
  }

  function onSaved() {
    closeModal();
    load();
  }
    useEffect(() => {
  fetchTeams()
    .then(setTeams)
    .catch(() => setTeams([]));
}, []);

  useEffect(() => {
    loadUsers();
  }, []);

 async function loadUsers(p = page) {
  const res = await fetchUsers({
    email: email || undefined,
    team_id: teamId || undefined,
    page: p,
    limit: pageSize
  });

  setUsers(res.results || []);
  setTotal(res.count || 0);
  setPage(p);
}



  async function toggleStatus(user) {
    if (user.user_id === currentUserId) return;
    await updateUserStatus(user.user_id, !user.is_active);
    load();
  }

  async function removeUser(user) {
    if (user.user_id === currentUserId) return;

    if (window.confirm(`Delete user ${user.email}? This action is irreversible.`)) {
      await deleteUser(user.user_id);
      load();
    }
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Manage Users</h2>
        <span className="text-muted small">
          You cannot modify your own account
        </span>
      </div>

      {error && (
        <div className="alert alert-danger py-2">{error}</div>
      )}
      <div className="card shadow-sm mb-3">
  <div className="card-body">
    <div className="row g-3 align-items-end">

      <div className="col-md-4">
        <label className="form-label">Email</label>
        <input
          className="form-control"
          placeholder="Search by email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
      </div>

      <div className="col-md-3">
        <label className="form-label">Team</label>
        <select
          className="form-select"
          value={teamId}
          onChange={e => setTeamId(e.target.value)}
        >
          <option value="">All Teams</option>
          {teams.map(t => (
            <option key={t.team_id} value={t.team_id}>
              {t.team_name}
            </option>
          ))}
        </select>
      </div>

      <div className="col-md-2">
        <label className="form-label">Rows</label>
        <select
          className="form-select"
          value={pageSize}
          onChange={e => {
            setPageSize(Number(e.target.value));
            setPage(1);
            loadUsers(1);
          }}
        >
          <option value={5}>5</option>
          <option value={10}>10</option>
          <option value={25}>25</option>
          <option value={50}>50</option>
        </select>
      </div>

      <div className="col-md-2">
        <button
          className="btn btn-primary w-100"
          onClick={() => loadUsers(1)}
        >
          Apply
        </button>
      </div>

    </div>
  </div>
</div>

      <table className="table table-hover align-middle">
        <thead className="table-light">
          <tr>
            <th>User</th>
            <th>Roles</th>
            <th>Teams</th>
            <th>Status</th>
            <th className="text-end">Actions</th>
          </tr>
        </thead>

        <tbody>
          {users.map(u => {
            const isSelf = u.user_id === currentUserId;

            return (
              <tr
                key={u.user_id}
                className={isSelf ? "table-warning" : ""}
              >
                <td>
                  <strong>{u.email}</strong>
                  <div className="text-muted small">
                    {u.username || "-"}
                    {isSelf && (
                      <span className="badge bg-secondary ms-2">You</span>
                    )}
                  </div>
                </td>

                <td>
                  {(u.roles || []).map(r => (
                    <span key={r} className="badge bg-primary me-1">
                      {r}
                    </span>
                  ))}
                </td>

                <td>
                  {(u.teams || []).map(t => (
                    <span key={t} className="badge bg-info text-dark me-1">
                      {t}
                    </span>
                  ))}
                </td>

                <td>
                  <span
                    className={`badge ${
                      u.is_active ? "bg-success" : "bg-secondary"
                    }`}
                  >
                    {u.is_active ? "Active" : "Inactive"}
                  </span>
                </td>

                <td className="text-end">
                  <button
                    className="btn btn-sm btn-outline-primary me-1"
                    onClick={() => onEdit(u)}  
                  >
                    Edit
                  </button>

                  <button
                    className="btn btn-sm btn-outline-warning me-1"
                    disabled={isSelf}
                    onClick={() => toggleStatus(u)}
                  >
                    {u.is_active ? "Deactivate" : "Activate"}
                  </button>

                  <button
                    className="btn btn-sm btn-outline-danger"
                    disabled={isSelf}
                    onClick={() => removeUser(u)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <div className="d-flex justify-content-end align-items-center gap-3 p-3 border-top">
        <button
          className="btn btn-outline-secondary btn-sm"
          disabled={page === 1}
          onClick={() => loadUsers(page - 1)}
        >
          Prev
        </button>

        <span>
          Page {page} of {Math.ceil(total / pageSize)}
        </span>

        <button
          className="btn btn-outline-secondary btn-sm"
          disabled={page >= Math.ceil(total / pageSize)}
          onClick={() => loadUsers(page + 1)}
        >
          Next
        </button>
      </div>


      {selectedUser && (
        <EditUserModal
          user={selectedUser}
          onClose={closeModal}
          onSaved={onSaved}
        />
      )}
    </>
  );
}
