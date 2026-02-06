// src/pages/AdminAudits.jsx
import { useEffect, useState } from "react";
import { fetchAuditLogs } from "../api/adminAudit.api";
import "bootstrap/dist/css/bootstrap.min.css";

export default function AdminAudits() {
  const [logs, setLogs] = useState([]);
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState({
    action_type: "",
    entity_type: ""
  });
  const [total, setTotal] = useState(0);

 const [limit, setLimit] = useState(10);

 useEffect(()=>{
  loadLogs(page);
 }, [page, filters, limit]);
  useEffect(() => {
    loadLogs(page);
  }, [page, filters]);

  async function loadLogs(p) {
    const res = await fetchAuditLogs(p, limit, filters);
    setLogs(res.results);
    setTotal(res.count);
  }

  return (
    <div className="container-fluid px-4 py-4">

      {/* HEADER */}
      <div className="mb-4">
        <h3 className="mb-1">Audit Logs</h3>
        <p className="text-muted mb-0">
          System activity and administrative actions
        </p>
      </div>

      {/* FILTERS */}
      <div className="card shadow-sm mb-3">
        <div className="card-body">
          <div className="row g-3">

            <div className="col-md-3">
              <label className="form-label">Action</label>
              <input
                className="form-control"
                placeholder="e.g. CREATE_USER"
                onChange={e => {
                  setPage(1);
                  setFilters({ ...filters, action_type: e.target.value });
                }}
              />
            </div>

            <div className="col-md-3">
              <label className="form-label">Entity</label>
              <input
                className="form-control"
                placeholder="e.g. USER, FILE"
                onChange={e => {
                  setPage(1);
                  setFilters({ ...filters, entity_type: e.target.value });
                }}
              />
            </div>
              <div className="col-md-3">
              <label className="form-label">Rows per page</label>
              <select
                className="form-select"
                
                value={limit}
                onChange={e => {
                  setLimit(parseInt(e.target.value, 10));
                  setPage(1);
                }}
              >
                <option value={5}>5</option>
                <option value={10}>10</option>
                <option value={25}>25</option>
                <option value={50}>50</option>
              </select>
              </div>
          </div>
        </div>
      </div>

      {/* TABLE */}
      <div className="card shadow-sm">
        <div className="table-responsive">
          <table className="table table-striped table-hover mb-0">
            <thead className="table-light">
              <tr>
                <th>Time</th>
                <th>User</th>
                <th>Action</th>
                <th>Entity</th>
                <th>Entity ID</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((l, i) => (
                <tr key={i}>
                  <td>{new Date(l.time).toLocaleString()}</td>
                  <td>{l.username || "-"}</td>
                  <td>
                    <span className="text-primary">
                      {l.action}
                    </span>
                  </td>
                  <td>{l.entity_type || "-"}</td>
                  <td>{l.entity_id || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* PAGINATION */}
        <div className="d-flex justify-content-end align-items-center gap-3 p-3 border-top">
          <button
            type="button"
            className="btn btn-outline-secondary btn-sm"
            disabled={page === 1}
            onClick={() => setPage(p => p - 1)}
          >
            Previous
          </button>

          <span className="fw-semibold">Page {page}</span>

          <button
            type="button"
            className="btn btn-outline-secondary btn-sm"
            disabled={page * limit >= total}
            onClick={() => setPage(p => p + 1)}
          >
            Next
          </button>
        </div>

      </div>

    </div>
  );
}
