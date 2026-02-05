import { useState } from "react";
import { Modal, Button, Spinner } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

import { changeMyPassword } from "../api/user.api";

export default function ChangePasswordModal({ show, onClose }) {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showCurrent, setShowCurrent] = useState(false);
  const [showNew, setShowNew] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  function resetForm() {
    setCurrentPassword("");
    setNewPassword("");
    setConfirmPassword("");
    setMessage("");
    setShowCurrent(false);
    setShowNew(false);
    setShowConfirm(false);
  }

  function handleClose() {
    resetForm();
    onClose();
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setMessage("");

    if (!currentPassword || !newPassword || !confirmPassword) {
      setMessage(" All fields are required");
      return;
    }

    if (newPassword !== confirmPassword) {
      setMessage(" New password and confirm password do not match");
      return;
    }

    try {
      setLoading(true);

      await changeMyPassword({
        current_password: currentPassword,
        new_password: newPassword
      });

      setMessage("Password changed successfully");
      alert("Password Changed Succesfully")
      // Close after user sees success
      setTimeout(handleClose, 1200);
    } catch (err) {
      setMessage(
        err.response?.data?.detail || " Failed to change password"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <Modal show={show} onHide={handleClose} centered backdrop="static">
      <Modal.Header closeButton>
        <Modal.Title>Change Password</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        {message && (
          <div
            className={`alert ${
              message.startsWith("✅") ? "alert-success" : "alert-danger"
            } py-2`}
          >
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* CURRENT PASSWORD */}
          <div className="mb-3">
            <label className="form-label">Current Password</label>
            <div className="input-group">
              <input
                type={showCurrent ? "text" : "password"}
                className="form-control"
                value={currentPassword}
                onChange={e => setCurrentPassword(e.target.value)}
              />
              <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={() => setShowCurrent(v => !v)}
              >
                {showCurrent ? "" : ""}
              </button>
            </div>
          </div>

          {/* NEW PASSWORD */}
          <div className="mb-3">
            <label className="form-label">New Password</label>
            <div className="input-group">
              <input
                type={showNew ? "text" : "password"}
                className="form-control"
                value={newPassword}
                onChange={e => setNewPassword(e.target.value)}
              />
              <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={() => setShowNew(v => !v)}
              >
                {showNew ? "" : ""}
              </button>
            </div>
          </div>

          {/* CONFIRM PASSWORD */}
          <div className="mb-3">
            <label className="form-label">Confirm New Password</label>
            <div className="input-group">
              <input
                type={showConfirm ? "text" : "password"}
                className="form-control"
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
              />
              <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={() => setShowConfirm(v => !v)}
              >
                {showConfirm ? "" : ""}
              </button>
            </div>
          </div>

          <div className="d-flex justify-content-end gap-2">
            <Button variant="secondary" onClick={handleClose}>
              Cancel
            </Button>

            <Button variant="primary" type="submit" disabled={loading}>
              {loading ? (
                <>
                  <Spinner size="sm" className="me-2" />
                  Saving...
                </>
              ) : (
                "Save Password"
              )}
            </Button>
          </div>
        </form>
      </Modal.Body>
    </Modal>
  );
}
