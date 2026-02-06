// src/pages/AdminSecurity.jsx
import { useEffect, useState } from "react";
import { fetchLoginHistory } from "../api/adminSecurity.api";
import "bootstrap/dist/css/bootstrap.min.css";

export default function AdminSecurity() {
  const [logs, setLogs] = useState([]);
  const [page, setPage] = useState(1);
  const [successFilter, setSuccessFilter] = useState("");
  const [total, setTotal] = useState(0);

  const [limit, setLimit] = useState(10);
  useEffect(() => {
  loadLogs(page);
}, [page, successFilter, limit]);


  useEffect(() => {
    loadLogs(page);
  }, [page, successFilter]);

  async function loadLogs(p) {
    const res = await fetchLoginHistory(
      p,
      limit,
      successFilter === "" ? undefined : successFilter === "true"
    );
    setLogs(res.results);
    setTotal(res.count);
  }

  return (
    <div className="container-fluid px-4 py-4">

      {/* HEADER */}
      <div className="mb-4">
        <h3 className="mb-1">Security Logs</h3>
        <p className="text-muted mb-0">
          Login attempts and authentication audit trail
        </p>
      </div>

      {/* FILTER */}
      <div className="card shadow-sm mb-3">
        <div className="card-body">
          <div className="row g-3 align-items-end">
            <div className="col-md-3">
              <label className="form-label">Status</label>
              <select
                className="form-select"
                value={successFilter}
                onChange={e => {
                  setPage(1);
                  setSuccessFilter(e.target.value);
                }}
              >
                <option value="">All</option>
                <option value="true">Successful</option>
                <option value="false">Failed</option>
              </select>
            </div>
            <div className="col-md-3">
              <label className="form-label">Rows per page</label>
              <select
                className="form-select"
                value={limit}
                onChange={e => {
                  setPage(1);
                  setLimit(parseInt(e.target.value));
                }}
              >
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="20">20</option>
                <option value="50">50</option>
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
                <th>IP Address</th>
                <th>Status</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((l, i) => (
                <tr key={i}>
                  <td>{new Date(l.login_time).toLocaleString()}</td>
                  <td>{l.username || "Unknown"}</td>
                  <td>{l.ip || "-"}</td>
                  <td>
                    <span
                      className={` ${
                        l.success ? "text-success" : "text-danger"
                      }`}
                    >
                      {l.success ? "SUCCESS" : "FAILED"}
                    </span>
                  </td>
                  <td>{l.failure_reason || "-"}</td>
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

          <span className="fw-semibold">
            Page {page}
          </span>

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
