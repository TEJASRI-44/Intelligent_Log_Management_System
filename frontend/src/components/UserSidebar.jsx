// src/components/user/UserSidebar.jsx
export default function UserSidebar({ activePage, setActivePage }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">LogHub Dashboard</div>
      </div>

      <nav className="sidebar-nav">
        
        <button className={`nav-item ${activePage === "search" ? "active" : ""}`}
          onClick={() => setActivePage("search")}>
          <span className="nav-text">Overview & Logs</span>
        </button>

        <button className={`nav-item ${activePage === "upload" ? "active" : ""}`}
          onClick={() => setActivePage("upload")}>
          <span className="nav-text">Upload Files</span>
        </button>

        <button className={`nav-item ${activePage === "files" ? "active" : ""}`}
          onClick={() => setActivePage("files")}>
          <span className="nav-text">My Files</span>
        </button>

        <button className={`nav-item ${activePage === "profile" ? "active" : ""}`}
          onClick={() => setActivePage("profile")}>
          <span className="nav-text">Profile</span>
        </button>
      </nav>
    </aside>
  );
}
