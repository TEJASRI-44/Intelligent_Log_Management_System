// src/pages/user/UserUploadFiles.jsx
import { useEffect, useState } from "react";
import { uploadLogFile } from "../api/files.api";
import { fetchMyTeams, fetchSources, fetchFormats } from "../api/lookups.api";
import {
  fetchAllowedSources,
  fetchAllowedFormats
} from "../api/lookups.api";
import { toast } from "react-toastify";

import "../styles/UserUploadFiles.css";

export default function UserUploadFiles() {
  const [teams, setTeams] = useState([]);
  const [sources, setSources] = useState([]);
  const [formats, setFormats] = useState([]);

  const [teamId, setTeamId] = useState("");
  const [sourceId, setSourceId] = useState("");
  const [formatId, setFormatId] = useState("");
  const [files, setFiles] = useState([]);
  



  const [loading, setLoading] = useState(false);
  

  /* ================= EFFECTS ================= */

  useEffect(() => {
    Promise.all([fetchMyTeams()])
      .then(([t]) => {
        setTeams(t);
      });
  }, []);

  useEffect(() => {
  if (!teamId) return;

  setSourceId("");
  setFormatId("");
  setSources([]);
  setFormats([]);

  fetchAllowedSources(teamId).then(setSources);
}, [teamId]);


useEffect(() => {
  if (!teamId || !sourceId) return;

  setFormatId("");
  setFormats([]);

  fetchAllowedFormats(teamId, sourceId).then(setFormats);
}, [teamId, sourceId]);


  /* ================= HANDLER ================= */

async function handleUpload(e) {
  e.preventDefault();

  if (!files.length) {
    toast.error("Please select at least one file to upload.");
    return;
  }

  setLoading(true);

  try {
    const response = await uploadLogFile(teamId, sourceId, formatId, files);

    const uploaded = response?.uploaded_files || [];
    const skipped = response?.skipped_files || [];

    if (uploaded.length > 0 && skipped.length === 0) {
      toast.success("Files uploaded successfully!");
    } 
    else if (uploaded.length > 0 && skipped.length > 0) {
      toast.warning(
        `${uploaded.length} uploaded, ${skipped.length} skipped`
      );
    } 
    else if (uploaded.length === 0 && skipped.length > 0) {
      toast.error(
        skipped.map(f => `${f.filename}: ${f.reason}`).join(", ")
      );
    } 
    else {
     toast.error("Duplicate files detected. Please upload new files.");

    }

   
    if (uploaded.length > 0) {
      setFiles([]);
      setTeamId("");
      setSourceId("");
      setFormatId("");
      e.target.reset();
    }

  } catch (err) {
    console.error(err);

    const backendMsg =
      err?.response?.data?.detail ||
      "Upload failed. Please try again.";

    toast.error(backendMsg);
  } finally {
    setLoading(false);
  }
}



  /* ================= RENDER ================= */

  return (
    <div className="user-upload-page">
      <div className="user-upload-header">
        <h1>Upload Log Files</h1>
        <p>Upload new log files for processing and analysis</p>
      </div>

      <div className="user-upload-card">
        <div className="user-upload-card-header">
          <h2>File Upload Form</h2>
        </div>

        <form className="user-upload-form" onSubmit={handleUpload}>
          <div className="user-upload-grid">

            <div className="user-upload-group">
              <label>Team</label>
              <select
                required
                value={teamId}
                onChange={e => setTeamId(e.target.value)}
              >
                <option value="">Select Team</option>
                {teams.map(t => (
                  <option key={t.team_id} value={t.team_id}>
                    {t.team_name}
                  </option>
                ))}
              </select>
            </div>

            <div className="user-upload-group">
              <label>Log Source</label>
              <select
                required
                value={sourceId}
                onChange={e => setSourceId(e.target.value)}
                disabled={!teamId}
                >
                <option value="">Select Source</option>
                {sources.map(s => (
                    <option key={s.source_id} value={s.source_id}>
                    {s.source_name}
                    </option>
                ))}
            </select>

            </div>

            <div className="user-upload-group">
              <label>File Format</label>
              <select
                required
                value={formatId}
                onChange={e => setFormatId(e.target.value)}
                disabled={!sourceId}
                >
                <option value="">Select Format</option>
                {formats.map(f => (
                    <option key={f.format_id} value={f.format_id}>
                    {f.format_name}
                    </option>
                ))}
              </select>

            </div>

            <div className="user-upload-group user-upload-full">
              <label>Log File</label>
              <input
                type="file"
                className="form-control"
                multiple
                onChange={(e) => setFiles(Array.from(e.target.files))}
              />
            </div>

          </div>

          <div className="user-upload-actions">
            <button
              type="submit"
              className="user-upload-btn"
              disabled={loading}
            >
              {loading ? "Uploading..." : "Upload File"}
            </button>
          </div>
        </form>

     {/*    {message && (
          <div className="user-upload-alert">
            {message}
          </div>
        )} */}
      </div>
    </div>
  );
}
