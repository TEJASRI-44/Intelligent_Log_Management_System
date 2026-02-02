import { useState, useEffect } from "react";
import { adminSearchLogs } from "../api/admin.api";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/AdminLogSearch.css";

export default function AdminLogSearch() {
  const [filters, setFilters] = useState({
    start_date: "",
    end_date: "",
    category: "",
    severity: "",
    keyword: ""
  });

  const [logs, setLogs] = useState([]);
  const [message, setMessage] = useState("");
const [pageSize, setPageSize] = useState(10);

  const [page, setPage] = useState(1);
  useEffect(() => {
    fetchLogs(page);
    // eslint-disable-next-line
  }, [page]);

  async function fetchLogs(newPage = 1) {
    setMessage("");
    setLogs([]);
    setPage(newPage);

    const payload = {
      ...filters,
      page: newPage,
      limit: pageSize,
      start_date: filters.start_date
        ? `${filters.start_date}T00:00:00`
        : undefined,
      end_date: filters.end_date
        ? `${filters.end_date}T23:59:59`
        : undefined
    };

    try {
      const res = await adminSearchLogs(payload);
      setLogs(res.results || []);
      setMessage(`Showing ${res.results?.length || 0} of ${res.count} logs`);
    } catch (err) {
      console.error(err);
      setMessage("Failed to search logs");
    }
  }

  useEffect(() => {
    fetchLogs(1);
    // eslint-disable-next-line
  }, []);

  function handleSearch(e) {
    e.preventDefault();
    fetchLogs(1);
  }
  function resetFilters(){
    const filters = {
    start_date: "",
    end_date: "",
    category: "",
    severity: "",
    keyword: ""
  };
    setFilters(filters);
    handleSearch(new Event("submit"));
    fetchLogs(1);
  }

  return (
    <div className="admin-log-search container-fluid px-4 py-4">

      {/* PAGE HEADER */}
      <div className="page-header mb-4">
        <h2>Audit & Log Search</h2>
        <p className="text-muted">
          Search, monitor and audit logs across all systems
        </p>
      </div>

      {/* FILTER CARD */}
     <div className="card shadow-sm mb-4 admin-log-filters">

        <div className="card-body">
          <form onSubmit={handleSearch}>
            <div className="row g-3">

              <div className="col-md-2">
                <label className="form-label">Keyword</label>
                <input
                  className="form-control"
                  placeholder="Search log message"
                  value={filters.keyword}
                  onChange={e =>
                    setFilters({ ...filters, keyword: e.target.value })
                  }
                />
              </div>

              <div className="col-md-2">
                <label className="form-label">Category</label>
                <select
                  className="form-select"
                  value={filters.category}
                  onChange={e =>
                    setFilters({ ...filters, category: e.target.value })
                  }
                >
                  <option value="">All</option>
                  <option>APPLICATION</option>
                  <option>SECURITY</option>
                  <option>INFRASTRUCTURE</option>
                  <option>AUDIT</option>
                </select>
              </div>

              <div className="col-md-2">
                <label className="form-label">Severity</label>
                <select
                  className="form-select"
                  value={filters.severity}
                  onChange={e =>
                    setFilters({ ...filters, severity: e.target.value })
                  }
                >
                  <option value="">All</option>
                  <option>INFO</option>
                  <option>WARN</option>
                  <option>ERROR</option>
                  <option>FATAL</option>
                </select>
              </div>

              <div className="col-md-2">
                <label className="form-label">From</label>
                <input
                  type="date"
                  className="form-control"
                  value={filters.start_date}
                  onChange={e =>
                    setFilters({ ...filters, start_date: e.target.value })
                  }
                />
              </div>

              <div className="col-md-2">
                <label className="form-label">To</label>
                <input
                  type="date"
                  className="form-control"
                  value={filters.end_date}
                  onChange={e =>
                    setFilters({ ...filters, end_date: e.target.value })
                  }
                />
              </div>
                  <div className="col-md-2">
                      <label className="form-label">Rows</label>
                      <select
                          className="form-select"
                          value={pageSize}
                          onChange={e => {
                          setPageSize(Number(e.target.value));
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
            <div className="col-md-1 d-grid align-self-end d-flex flex-row gap-2">
                <button className="btn btn-primary">
                  Search
                </button>
                <button  className="btn btn-outline-primary mt-3  " onClick={resetFilters}>
                  Reset
                </button>
            </div>
            

          </form>

        </div>
      </div>

      {/* MESSAGE */}
      {message && (
        <div className="alert alert-info py-2">
          {message}
        </div>
      )}

      {/* RESULTS TABLE */}
      <div className="card shadow-sm">
        <div className="table-responsive">
          <table className="table table-hover align-middle mb-0">
            <thead className="table-light">
              <tr>
                <th>Timestamp</th>
                <th>Severity</th>
                <th>Category</th>
                <th>Service</th>
                <th>Message</th>
              </tr>
            </thead>
            <tbody>

              {logs.length === 0 ? (
                <tr>
                  <td colSpan="5" className="text-center text-muted py-4">
                    No logs found
                  </td>
                </tr>
              ) : (
                logs.map((l, i) => (
                  <tr key={i}>
                    <td>{new Date(l.timestamp).toLocaleString()}</td>
                    <td>
                      <span className={`severity-badge ${l.severity}`}>
                        {l.severity}
                      </span>
                    </td>
                    <td>{l.category}</td>
                    <td>{l.service || "-"}</td>
                    <td className="log-message">
                      {l.message}
                    </td>
                  </tr>
                ))
              )}

            </tbody>
          </table>
        </div>

        {/* PAGINATION */}
        <div className="d-flex justify-content-end align-items-center gap-3 p-3 border-top">
          <button
            type="button"
            className="btn btn-outline-secondary btn-sm"
            disabled={page === 1}
            onClick={() => fetchLogs(page - 1)}
          >
            Prev
          </button>

          <span className="fw-semibold">Page {page}</span>

          <button
            type="button"
            className="btn btn-outline-secondary btn-sm"
            onClick={() => fetchLogs(page + 1)}
          >
            Next
          </button>
        </div>
      </div>

    </div>
  );
}
