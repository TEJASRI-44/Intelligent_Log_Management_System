import { useEffect, useState } from "react";
import {
  fetchLogsPerDay,
  fetchTopErrors,
  fetchActiveSystems,
  fetchRecentLogs
} from "../api/adminReports.api";
import "bootstrap/dist/css/bootstrap.min.css";

export default function AdminReports() {
  /* ================= STATE ================= */

  const [logsPerDay, setLogsPerDay] = useState([]);
  const [topErrors, setTopErrors] = useState([]);
  const [systems, setSystems] = useState([]);
  const [recentLogs, setRecentLogs] = useState([]);
  const [recentDays, setRecentDays] = useState(10);

  const [error, setError] = useState("");

  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedDateLogs, setSelectedDateLogs] = useState(0);

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [activeSection, setActiveSection] = useState("ALL");
// ALL | TOP_ERRORS | ACTIVE_SYSTEMS

  const totalErrorCount = topErrors.reduce(
  (sum, err) => sum + err.count,
  0
);

  /* pagination */
  const [page, setPage] = useState(1);
  const pageSize = 10;

  /* ================= LOAD ================= */

  useEffect(() => {
    loadReports();
  }, []);

  useEffect(() => {
  loadRecentLogs();
}, [page, recentDays]);

  useEffect(() => {
    loadRecentLogs();
  }, [page]);

  async function loadReports() {
    try {
      setLogsPerDay(await fetchLogsPerDay());
      setTopErrors(await fetchTopErrors());
    } catch {
      setError("Failed to load reports");
    }
  }

  async function loadRecentLogs() {
  try {
    const res = await fetchRecentLogs(recentDays, page, pageSize);
    setRecentLogs(res.results || []);
  } catch {
    setRecentLogs([]);
  }
}

  function handleDateChange(e) {
    const date = e.target.value;
    setSelectedDate(date);

    const match = logsPerDay.find(r => r.log_date === date);
    setSelectedDateLogs(match ? match.total_logs : 0);
  }

  async function loadActiveSystems() {
    try {
      const res = await fetchActiveSystems(startDate, endDate);
      setSystems(res || []);
    } catch {
      setSystems([]);
    }
  }

  /* ================= UI ================= */

  return (
    <div className="container-fluid px-4 py-4">

      {/* HEADER */}
      <div className="mb-4">
        <h3 className="mb-1">System Reports</h3>
        <p className="text-muted mb-0">
          Operational insights and system activity overview
        </p>
      </div>
      {activeSection !== "ALL" && (
  <button
    className="btn btn-outline-secondary btn-sm mb-3"
    onClick={() => setActiveSection("ALL")}
  >
    ← Back to Reports
  </button>
)}

      {error && (
        <div className="alert alert-danger py-2">{error}</div>
      )}

      {/* ================= LOGS BY DATE ================= */}
      {activeSection === "ALL" && (
  <div className="card shadow-sm mb-4">
    <div className="card-body">
      <h5 className="card-title mb-3">Logs by Date</h5>

      <div className="d-flex align-items-center gap-3">
        <input
          type="date"
          className="form-control w-auto"
          value={selectedDate}
          onChange={handleDateChange}
        />

        {selectedDate && (
          <span className="badge bg-primary fs-6">
            {selectedDateLogs} logs
          </span>
        )}
      </div>
    </div>
  </div>
)}

      {activeSection === "ALL" && (
  <div className="row g-4 mb-4">

    <div className="col-md-6">
  <div
    className="card shadow-sm h-100"
    style={{ cursor: "pointer" }}
    onClick={() => setActiveSection("TOP_ERRORS")}
  >
    <div className="card-body">
      <h6 className="text-muted">Top Errors</h6>

      <h3 className="text-danger">
        {totalErrorCount}
      </h3>

      <p className="text-muted mb-0">
        View Detailed breakdown of top error types
      </p>
    </div>
  </div>
</div>


    <div className="col-md-6">
      <div
        className="card shadow-sm h-100"
        style={{ cursor: "pointer" }}
        onClick={() => setActiveSection("ACTIVE_SYSTEMS")}
      >
        <div className="card-body">
          <h6 className="text-muted">Active Systems</h6>
          <br />
          <div>
            <p className="text-muted mb-0">View system activity</p>
          </div>
        </div>
      </div>
    </div>

  </div>
)}


      {/* ================= TOP ERRORS ================= */}
      {activeSection === "TOP_ERRORS" && (
  <div className="card shadow-sm mb-4">
    <div className="card-body">
      <h5 className="card-title mb-1">Top Error Types</h5>
      <p className="text-muted mb-3">
        Most frequent critical failures with recent samples
      </p>

      {topErrors.map(err => (
        <div key={err.severity} className="mb-4">
          <div className="d-flex align-items-center gap-2 mb-2">
            <span className="badge bg-danger">{err.severity}</span>
            <strong>{err.count} occurrences</strong>
          </div>

          <div className="table-responsive">
            <table className="table table-sm table-striped table-bordered">
              <thead className="table-light">
                <tr>
                  <th>Timestamp</th>
                  <th>Service</th>
                  <th>Message</th>
                </tr>
              </thead>
              <tbody>
                {err.sample_logs.map((l, i) => (
                  <tr key={i}>
                    <td>{new Date(l.timestamp).toLocaleString()}</td>
                    <td>{l.service || "-"}</td>
                    <td>{l.message}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  </div>
)}


      {/* ================= ACTIVE SYSTEMS ================= */}
      {activeSection === "ACTIVE_SYSTEMS" && (
  <div className="card shadow-sm mb-4">
    <div className="card-body">
      <h5 className="card-title mb-3">Most Active Systems</h5>

      <div className="row g-2 align-items-end mb-3">
        <div className="col-md-3">
          <label className="form-label">Start Date</label>
          <input
            type="date"
            className="form-control"
            onChange={e => setStartDate(e.target.value)}
          />
        </div>

        <div className="col-md-3">
          <label className="form-label">End Date</label>
          <input
            type="date"
            className="form-control"
            onChange={e => setEndDate(e.target.value)}
          />
        </div>

        <div className="col-md-2">
          <button
            className="btn btn-primary w-100"
            onClick={loadActiveSystems}
          >
            Apply
          </button>
        </div>
      </div>

      <ul className="list-group list-group-flush">
        {systems.map(sys => (
          <li
            key={sys.service_name}
            className="list-group-item d-flex justify-content-between"
          >
            <span>{sys.service_name}</span>
            <span className="badge bg-secondary">
              {sys.log_count} logs
            </span>
          </li>
        ))}
      </ul>
    </div>
  </div>
)}

      {/* ================= RECENT LOGS ================= */}
<div className="card shadow-sm">
  <div className="card-body">
    <div className="d-flex justify-content-between align-items-center mb-3">
      <h5 className="card-title mb-0">Recent Logs</h5>

      <select
        className="form-select w-auto"
        value={recentDays}
        onChange={e => {
          setPage(1);
          setRecentDays(Number(e.target.value));
        }}
      >
        <option value={2}>Last 2 days</option>
        <option value={5}>Last 5 days</option>
        <option value={10}>Last 10 days</option>
        <option value={15}>Last 15 days</option>
        <option value={30}>Last 30 days</option>
      </select>
    </div>

    {recentLogs.length === 0 ? (
      <div className="text-muted">
        No logs found for selected range
      </div>
    ) : (
      <>
        <div className="table-responsive">
          <table className="table table-hover table-striped table-bordered mb-0">
            <thead className="table-light">
              <tr>
                <th>Timestamp</th>
                <th>Severity</th>
                <th>Service</th>
                <th>Message</th>
              </tr>
            </thead>
            <tbody>
              {recentLogs.map((l, i) => (
                <tr key={i}>
                  <td>{new Date(l.timestamp).toLocaleString()}</td>
                  <td>
                    <span className={` ${
                      l.severity === "ERROR"
                        ? "text-danger"
                        : l.severity === "WARN"
                        ? "text-warning text-dark"
                        : "text-info"
                    }`}>
                      {l.severity}
                    </span>
                  </td>
                  <td>{l.service || "-"}</td>
                  <td>{l.message}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="d-flex justify-content-end align-items-center gap-3 mt-3">
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
            onClick={() => setPage(p => p + 1)}
          >
            Next
          </button>
        </div>
      </>
    )}
  </div>
</div>
    </div>
  );
}
