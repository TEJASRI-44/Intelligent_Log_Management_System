import { useEffect, useState } from "react";
import { uploadLogFile } from "../api/files.api";
import { fetchMyTeams, fetchAllowedSources, fetchAllowedFormats } from "../api/lookups.api";
import { toast } from "react-toastify";

export default function AdminUploadModal({ show, onClose, onSuccess }) {
  const [teams, setTeams] = useState([]);
  const [sources, setSources] = useState([]);
  const [formats, setFormats] = useState([]);

  const [teamId, setTeamId] = useState("");
  const [sourceId, setSourceId] = useState("");
  const [formatId, setFormatId] = useState("");
  const [files, setFiles] = useState([]);

  const [loading, setLoading] = useState(false);

  // 1. Fetch only Teams when modal opens
  useEffect(() => {
    if (show) {
      fetchMyTeams()
        .then(data => setTeams(data))
        .catch(err => console.error("Error fetching teams:", err));
    } else {
      // Reset state when modal closes
      setTeamId("");
      setSourceId("");
      setFormatId("");
      setSources([]);
      setFormats([]);
    }
  }, [show]);

  // 2. Fetch Sources whenever teamId changes
  useEffect(() => {
    if (teamId) {
      fetchAllowedSources(teamId)
        .then(data => {
          setSources(data);
          setSourceId(""); // Reset source when team changes
          setFormats([]);  // Clear formats until a source is picked
        })
        .catch(err => console.error("Error fetching sources:", err));
    }
  }, [teamId]);

  // 3. Fetch Formats whenever sourceId changes
  useEffect(() => {
    if (teamId && sourceId) {
      fetchAllowedFormats(teamId, sourceId)
        .then(data => setFormats(data))
        .catch(err => console.error("Error fetching formats:", err));
    }
  }, [teamId, sourceId]);

  async function handleUpload(e) {
    e.preventDefault();
    if (!files || !teamId || !sourceId || !formatId) return;

    setLoading(true);
    try {
      await uploadLogFile(teamId, sourceId, formatId, files);
      toast.success("Files uploaded Successfully")
      onSuccess();
      onClose();
    } catch (err) {
      alert("Upload failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  }

  if (!show) return null;

  return (
    <div className="modal fade show d-block" style={{ background: "rgba(0,0,0,.5)" }}>
      <div className="modal-dialog modal-lg modal-dialog-centered m-auto">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Upload Log File</h5>
            <button className="btn-close" onClick={onClose}><i class="bi text-black bi-x-lg"></i></button>
          </div>

          <form onSubmit={handleUpload}>
            <div className="modal-body">
              <div className="row g-3">
                
                {/* Team Selection */}
                <div className="col-md-4">
                  <label className="form-label">Team</label>
                  <select 
                    className="form-select" 
                    required 
                    value={teamId}
                    onChange={e => setTeamId(e.target.value)}
                  >
                    <option value="">Select Team</option>
                    {teams.map(t => (
                      <option key={t.team_id} value={t.team_id}>{t.team_name}</option>
                    ))}
                  </select>
                </div>

                {/* Source Selection - Only enabled if Team is selected */}
                <div className="col-md-4">
                  <label className="form-label">Source</label>
                  <select 
                    className="form-select" 
                    required 
                    value={sourceId}
                    disabled={!teamId}
                    onChange={e => setSourceId(e.target.value)}
                  >
                    <option value="">Select Source</option>
                    {sources.map(s => (
                      <option key={s.source_id} value={s.source_id}>{s.source_name}</option>
                    ))}
                  </select>
                </div>

                {/* Format Selection - Only enabled if Source is selected */}
                <div className="col-md-4">
                  <label className="form-label">Format</label>
                  <select 
                    className="form-select" 
                    required 
                    value={formatId}
                    disabled={!sourceId}
                    onChange={e => setFormatId(e.target.value)}
                  >
                    <option value="">Select Format</option>
                    {formats.map(f => (
                      <option key={f.format_id} value={f.format_id}>{f.format_name}</option>
                    ))}
                  </select>
                </div>

                <div className="col-12">
                  <label className="form-label">File</label>
                 <input 
                    type="file" 
                    className="form-control" 
                    multiple
                    required 
                    onChange={(e) => setFiles(Array.from(e.target.files))}
                  />

                </div>

              </div>
            </div>

            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={loading || !files}>
                {loading ? "Uploading..." : "Upload"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}