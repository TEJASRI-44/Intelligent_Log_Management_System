// src/pages/user/UserMyFiles.jsx
import { useEffect, useState } from "react";
import {
  fetchMyFiles,
  deleteMyFile,
  restoreMyFile,
  userDownloadFile
} from "../api/files.api";
import { fetchMyTeams } from "../api/lookups.api";
import "bootstrap/dist/css/bootstrap.min.css";

export default function UserMyFiles() {
  const [files, setFiles] = useState([]);
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [totalFiles, setTotalFiles] = useState(0);
  const [filters, setFilters] = useState({ name: "" });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMyTeams().then(setTeams);
  }, []);

  useEffect(() => {
    loadFiles();
  }, [page, pageSize, selectedTeam]);

  async function loadFiles() {
    setLoading(true);
    try {
      const res = await fetchMyFiles({
        name: filters.name || undefined,
        team_id: selectedTeam || undefined,
        page,
        limit: pageSize
      });
      setFiles(res.results || []);
      setTotalFiles(res.count || 0);
    } catch {
      setFiles([]);
      setTotalFiles(0);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete this file?")) return;
    await deleteMyFile(id);
    loadFiles();
  }

  async function handleRestore(id) {
    await restoreMyFile(id);
    loadFiles();
  }

  return (
    <div className="container-fluid px-3 px-md-4 py-4">

      {/* HEADER */}
      <div className="mb-4">
        <h2 className="mb-1">My Files</h2>
        <p className="text-muted mb-0">
          Files uploaded by you across your teams
        </p>
      </div>

      {/* FILTERS */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <div className="row g-3 align-items-end">

            <div className="col-12 col-md-4">
              <label className="form-label">File Name</label>
              <input
                className="form-control"
                placeholder="Search by file name"
                onChange={e =>
                  setFilters({ ...filters, name: e.target.value })
                }
              />
            </div>

            <div className="col-12 col-md-4">
              <label className="form-label">Team</label>
              <select
                className="form-select"
                value={selectedTeam}
                onChange={e => {
                  setSelectedTeam(e.target.value);
                  setPage(1);
                }}
              >
                <option value="">All My Teams</option>
                {teams.map(t => (
                  <option key={t.team_id} value={t.team_id}>
                    {t.team_name}
                  </option>
                ))}
              </select>
            </div>

            <div className="col-6 col-md-2">
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

            {/* <div className="col-6 col-md-2">
              <button
                className="btn btn-primary w-100"
                onClick={() => {
                  setPage(1);
                  loadFiles();
                }}
              >
                Apply
              </button>
            </div>
 */}
          </div>
        </div>
      </div>

      {/* TABLE */}
      <div className="card shadow-sm">
        <div className="card-body">

          <div className="table-responsive">
            <table className="table table-hover  align-middle mb-0">
              <thead className="table-light">
                <tr>
                  <th>Name</th>
                  <th>Team</th>
                  <th>Uploaded At</th>
                  <th>Size</th>
                  <th>Status</th>
                  <th className="text-end">Action</th>
                </tr>
              </thead>

              <tbody>
                {loading && (
                  <tr>
                    <td colSpan="6" className="text-center text-muted">
                      Loading...
                    </td>
                  </tr>
                )}

                {!loading && files.length === 0 && (
                  <tr>
                    <td colSpan="6" className="text-center text-muted">
                      No files found
                    </td>
                  </tr>
                )}

                {files.map(f => (
                  <tr
                    key={f.file_id}
                    className={f.is_deleted ? "table-secondary" : ""}
                  >
                    <td>{f.name}</td>
                    <td>{f.team}</td>
                    <td>{new Date(f.uploaded_at).toLocaleString()}</td>
                    <td>{(f.file_size / 1024).toFixed(1)} KB</td>
                    <td>
                      <span className="badge bg-primary">
                        {f.status}
                      </span>
                    </td>
                    <td className="text-end">
                      {f.is_deleted ? (
                        <button
                          className="btn btn-sm btn-success"
                          onClick={() => handleRestore(f.file_id)}
                        >
                          Restore
                        </button>
                      ) : (
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => handleDelete(f.file_id)}
                        >
                          Delete
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* PAGINATION */}
          <div className="d-flex flex-column flex-sm-row justify-content-between align-items-center gap-2 mt-3">
            <button
              className="btn btn-outline-secondary btn-sm"
              disabled={page === 1}
              onClick={() => setPage(p => p - 1)}
            >
              Prev
            </button>

            <span className="fw-semibold">
              Page {page} of {Math.ceil(totalFiles / pageSize) || 1}
            </span>

            <button
              className="btn btn-outline-secondary btn-sm"
              disabled={page >= Math.ceil(totalFiles / pageSize)}
              onClick={() => setPage(p => p + 1)}
            >
              Next
            </button>
          </div>

        </div>
      </div>

    </div>
  );
}
