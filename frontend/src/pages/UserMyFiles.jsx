// src/pages/user/UserMyFiles.jsx
import { useEffect, useState } from "react";
import { fetchMyFiles, deleteMyFile, restoreMyFile, userDownloadFile } from "../api/files.api";
import { fetchMyTeams } from "../api/lookups.api";
import "../styles/UserMyFiles.css";

export default function UserMyFiles() {
  const [files, setFiles] = useState([]);
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [totalFiles, setTotalFiles] = useState(0);
  const [filters, setFilters] = useState({ name: "" });
  const [loading, setLoading] = useState(false);

  /* ================= EFFECTS ================= */

  useEffect(() => {
    fetchMyTeams().then(setTeams);
  }, []);

  useEffect(() => {
    loadFiles();
  }, [page, pageSize, selectedTeam]);

  /* ================= LOAD FILES ================= */

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

  } catch (err) {
    console.error("Failed to load files", err);
    setFiles([]);
    setTotalFiles(0);
  } finally {
    setLoading(false);
  }
}

    async function handleDelete(fileId) {
        if (!window.confirm("Delete this file?")) return;

        try {
            await deleteMyFile(fileId);
            await loadFiles(); 
        } catch (err) {
            console.error("Delete failed", err);
        }
    }
    async function handleRestore(fileId) {
        try {
            await restoreMyFile(fileId);
            await loadFiles();
        } catch (err) {
            console.error("Restore failed", err);
        }
    }

  /* ================= RENDER ================= */

  return (
    <div className="user-files-page">
      {/* HEADER */}
      <div className="user-files-header">
        <h1>My Files</h1>
        <p>Files uploaded by you across your teams</p>
      </div>

      {/* FILTERS */}
      <div className="user-files-filter-card">
        <div className="user-files-filter-body">
          <div className="user-files-filter-grid">

            <div className="user-files-filter-group">
              <label>File Name</label>
              <input
                placeholder="Search by file name"
                onChange={e =>
                  setFilters({ ...filters, name: e.target.value })
                }
              />
            </div>

            <div className="user-files-filter-group">
              <label>Team</label>
              <select
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

            <div className="user-files-filter-group small">
              <label>Rows</label>
              <select
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

            <div className="user-files-filter-group action">
              <button
                className="user-files-apply-btn"
                onClick={() => {
                  setPage(1);
                  loadFiles();
                }}
              >
                Apply
              </button>
            </div>

          </div>
        </div>
      </div>

      {/* TABLE */}
      <div className="user-files-card">
        <div className="user-files-table-container">
          <table className="user-files-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Team</th>
                <th>Uploaded At</th>
                <th>Size</th>
                <th className="align-right">Status</th>
              </tr>
            </thead>

            <tbody>
              {!Array.isArray(files) && (
                <tr>
                  <td colSpan="5" className="user-files-error">
                    ERROR: files is not an array
                  </td>
                </tr>
              )}

              {Array.isArray(files) && files.length === 0 && !loading && (
                <tr>
                  <td colSpan="5" className="user-files-empty">
                    No files found
                  </td>
                </tr>
              )}

              {Array.isArray(files) &&
                files.map(f => (
                  <tr
                    key={f.file_id}
                    className={f.is_deleted ? "user-files-row-deleted" : ""}
                  >
                    <td>{f.name}</td>
                    <td>{f.team}</td>
                    <td>{new Date(f.uploaded_at).toLocaleString()}</td>
                    <td>{(f.file_size / 1024).toFixed(1)} KB</td>
                    <td>
                      <span className={`badge ${
                        "bg-primary"
                      }`}>
                        {f.status}
                      </span>
                    </td>

                    <td className="align-right">
                         {/* <button
                            className="btn btn-sm btn-outline-primary"
                            disabled={f.is_deleted || f.status === "ARCHIVED"}
                            title={
                            f.is_deleted
                                ? "File is deleted"
                                : f.status === "ARCHIVED"
                                ? "Archived files cannot be downloaded"
                                : "Download file"
                            }
                            onClick={() => userDownloadFile(f.file_id)}
                        >
                            Download
                        </button> */}
                      {f.is_deleted ? (
                        <button
                        type="button"
                          className="user-files-restore-btn"
                          onClick={() => handleRestore(f.file_id)}
                        >
                          Restore
                        </button>
                      ) : (
                        <button
                            type="button"
                            className="user-files-delete-btn"
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
        <div className="user-files-pagination">
          <button
            type="button"
            disabled={page === 1}
            onClick={() => setPage(p => p - 1)}
          >
            Prev
          </button>

          <span>
            Page {page} of {Math.ceil(totalFiles / pageSize) || 1}
          </span>

          <button
            type="button"
            disabled={page >= Math.ceil(totalFiles / pageSize)}
            onClick={() => setPage(p => p + 1)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
