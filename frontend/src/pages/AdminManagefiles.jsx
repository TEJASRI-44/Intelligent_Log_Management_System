import { useEffect, useState } from "react";
import { fetchAdminFiles, adminDeleteFile } from "../api/admin.api";
import "bootstrap/dist/css/bootstrap.min.css";
import AdminUploadModal from "./AdminUploadModal";
import { adminRestoreFile } from "../api/admin.api";
import { fetchTeams } from "../api/lookups.api";
import { adminDownloadFile } from "../api/admin.api";
import { runLogRetention } from "../api/admin.api";


export default function AdminManageFiles() {
  const [files, setFiles] = useState([]);
  const [filters, setFilters] = useState({
    start_date: "",
    end_date: "",
    name: ""
  });
  const [loading, setLoading] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [teams, setTeams] = useState([]);
const [selectedTeam, setSelectedTeam] = useState("");
const [page, setPage] = useState(1);
const [pageSize, setPageSize] = useState(10);
const [total, setTotal] = useState(0);

 useEffect(() => {
  fetchTeams().then(setTeams);
}, []);

  useEffect(() => {
    loadFiles();
  }, []);

 async function loadFiles() {
  setLoading(true);

  const params = {
    ...filters,
    team_id: selectedTeam || undefined,
    page,
    limit: pageSize,
    start_date: filters.start_date
      ? `${filters.start_date}T00:00:00`
      : undefined,
    end_date: filters.end_date
      ? `${filters.end_date}T23:59:59`
      : undefined,
  };

  const res = await fetchAdminFiles(params);
  setFiles(res.results);
  setTotal(res.count);
  setLoading(false);
}
console.log(files);

  async function handleDelete(id) {
    if (!window.confirm("Delete this file permanently?")) return;
    await adminDeleteFile(id);
    loadFiles();
  }
  async function handleRestore(fileId) {
  if (!window.confirm("Restore this file?")) return;

  await adminRestoreFile(fileId);
  loadFiles();
}


  return (
    <div className="container-fluid px-4 py-4">
    <div className="d-flex justify-content-between align-items-center mb-3">
    <div>
        <h2 className="mb-1"> Uploaded Files</h2>
        <p className="text-muted mb-0">View and manage all uploaded log files</p>
    </div>
    <button
      className="btn btn-outline-warning"
      onClick={runLogRetention}
    >
      Archive Old Files
    </button>

    <button className="btn btn-primary" onClick={() => setShowUpload(true)}>
        Upload File
    </button>
    </div>
    <AdminUploadModal
    show={showUpload}
    onClose={() => setShowUpload(false)}
    onSuccess={loadFiles}
    />


      {/* Filters */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <div className="row g-3 align-items-end">
            <div className="col-md-4">
              <label className="form-label">File Name</label>
              <input
                className="form-control"
                placeholder="Search by name"
                onChange={e =>
                  setFilters({ ...filters, name: e.target.value })
                }
              />
            </div>
            <div className="col-md-3">
              <label className="form-label">From</label>
              <input
                type="date"
                className="form-control"
                onChange={e =>
                  setFilters({ ...filters, start_date: e.target.value })
                }
              />
            </div>
            <div className="col-md-3">
              <label className="form-label">To</label>
              <input
                type="date"
                className="form-control"
                onChange={e =>
                  setFilters({ ...filters, end_date: e.target.value })
                }
              />
            </div>
            <div className="col-md-3">
            <label className="form-label">Team</label>
            <select
                className="form-select"
                onChange={e => setSelectedTeam(e.target.value)}
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
                onClick={loadFiles}
              >
                Apply
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="card shadow-sm">
        <div className="table-responsive">
          <table className="table table-hover align-middle mb-0">
            <thead className="table-light">
              <tr>
                <th>Name</th>
                <th>Team</th>
                <th>Uploaded By</th>
                <th>Date</th>
                <th>Size</th>
                <th>Status</th>

                <th></th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="6" className="text-center py-4">
                    Loading...
                  </td>
                </tr>
              ) : files.length === 0 ? (
                <tr>
                  <td colSpan="6" className="text-center py-4 text-muted">
                    No files found
                  </td>
                </tr>
              ) : (
                files.map(f => (
                <tr key={f.file_id} className={f.is_deleted ? "table-secondary" : ""}>
                    <td className="fw-semibold">{f.name}</td>
                    <td>{f.team}</td>
                    <td>{f.uploaded_by}</td>
                    <td>{new Date(f.uploaded_at).toLocaleString()}</td>
                    <td>{(f.file_size / 1024).toFixed(1)} KB</td>
                   <td>
                      <span className={`badge ${
                        "bg-primary"
                      }`}>
                        {f.status}
                      </span>
                    </td>

                    <td className="text-end">
                    <button
                      className="btn btn-sm btn-outline-primary"
                      disabled={f.is_deleted || f.status === "ARCHIVED"}
                      title={
                        f.is_deleted
                          ? "File is deleted"
                          : f.status === "ARCHIVED"
                          ? "Archived files cannot be downloaded"
                          : "Download file"
                      }
                      onClick={() => adminDownloadFile(f.file_id)}
                    >
                      Download
                    </button>

                    {f.is_deleted ? (
                        <button
                        className="btn btn-sm btn-outline-success"
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
                ))

              )}
            </tbody>
          </table>
        </div>
        <div className="d-flex justify-content-end align-items-center gap-3 p-3 border-top">
  <button
    className="btn btn-outline-secondary btn-sm"
    disabled={page === 1}
    onClick={() => setPage(p => p - 1)}
    type="button"
  >
    Prev
  </button>

  <span>
    Page {page} of {Math.ceil(total / pageSize)}
  </span>

  <button
    type="button"
    className="btn btn-outline-secondary btn-sm"
    disabled={page >= Math.ceil(total / pageSize)}
    onClick={() => setPage(p => p + 1)}
  >
    Next
  </button>
</div>

      </div>
    </div>
  );
}
