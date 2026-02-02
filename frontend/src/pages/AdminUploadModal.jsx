import { useEffect, useState } from "react";
import { uploadLogFile } from "../api/files.api";
import { fetchTeams, fetchSources, fetchFormats } from "../api/lookups.api";

export default function AdminUploadModal({ show, onClose, onSuccess }) {
  const [teams, setTeams] = useState([]);
  const [sources, setSources] = useState([]);
  const [formats, setFormats] = useState([]);

  const [teamId, setTeamId] = useState("");
  const [sourceId, setSourceId] = useState("");
  const [formatId, setFormatId] = useState("");
  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (show) {
      Promise.all([
        fetchTeams(),
        fetchSources(),
        fetchFormats()
      ]).then(([t, s, f]) => {
        setTeams(t);
        setSources(s);
        setFormats(f);
      });
    }
  }, [show]);

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    await uploadLogFile(teamId, sourceId, formatId, file);
    setLoading(false);

    onSuccess();
    onClose();
  }

  if (!show) return null;

  return (
    <div className="modal fade show d-block" style={{ background: "rgba(0,0,0,.5)" }}>
      <div className="modal-dialog modal-lg">
        <div className="modal-content">

          <div className="modal-header">
            <h5 className="modal-title">Upload Log File</h5>
            <button className="btn-close" onClick={onClose}></button>
          </div>

          <form onSubmit={handleUpload}>
            <div className="modal-body">
              <div className="row g-3">

                <div className="col-md-4">
                  <label className="form-label">Team</label>
                  <select className="form-select" required onChange={e => setTeamId(e.target.value)}>
                    <option value="">Select</option>
                    {teams.map(t => <option key={t.team_id} value={t.team_id}>{t.team_name}</option>)}
                  </select>
                </div>

                <div className="col-md-4">
                  <label className="form-label">Source</label>
                  <select className="form-select" required onChange={e => setSourceId(e.target.value)}>
                    <option value="">Select</option>
                    {sources.map(s => <option key={s.source_id} value={s.source_id}>{s.source_name}</option>)}
                  </select>
                </div>

                <div className="col-md-4">
                  <label className="form-label">Format</label>
                  <select className="form-select" required onChange={e => setFormatId(e.target.value)}>
                    <option value="">Select</option>
                    {formats.map(f => <option key={f.format_id} value={f.format_id}>{f.format_name}</option>)}
                  </select>
                </div>

                <div className="col-12">
                  <label className="form-label">File</label>
                  <input type="file" className="form-control" required onChange={e => setFile(e.target.files[0])} />
                </div>

              </div>
            </div>

            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? "Uploading..." : "Upload"}
              </button>
            </div>
          </form>

        </div>
      </div>
    </div>
  );
}
