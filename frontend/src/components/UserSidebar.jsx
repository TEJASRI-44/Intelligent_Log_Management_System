import { useState } from "react";
import { NavLink } from "react-router-dom";
import "../styles/UserSidebar.css";

export default function UserSidebar() {
  const [isOpen, setIsOpen] = useState(false);

  const closeSidebar = () => setIsOpen(false);

  return (
    <>
     
      <button
        className="btn  fixed-top btn-sm mobile-toggle-btn"
        style={{width:"10px"}}
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? <i class="bi text-white bi-x-lg"></i>
: <i class="bi bi-list"></i>


}
      </button>

      {isOpen && (
        <div 
          className="sidebar-overlay d-md-none" 
          onClick={closeSidebar}
        ></div>
      )}

      <aside className={`sidebar bg-dark border-end ${isOpen ? "open" : ""}`}>
        
        <div className="sidebar-brand text-white fw-bold fs-5">
          User Dashboard
        </div>

        <nav className="nav nav-pills flex-column gap-2 px-3">
          <NavLink
            to="/user/logs"
            onClick={closeSidebar}
            className={({ isActive }) =>
              `nav-link ${isActive ? "active bg-primary" : "text-white link-hover"}`
            }
          >
            Overview & Logs
          </NavLink>

          <NavLink
            to="/user/upload-file"
            onClick={closeSidebar}
            className={({ isActive }) =>
              `nav-link ${isActive ? "active bg-primary" : "text-white link-hover"}`
            }
          >
            Upload Files
          </NavLink>

          <NavLink
            to="/user/my-files"
            onClick={closeSidebar}
            className={({ isActive }) =>
              `nav-link ${isActive ? "active bg-primary" : "text-white link-hover"}`
            }
          >
            My Files
          </NavLink>

          <NavLink
            to="/user/profile"
            onClick={closeSidebar}
            className={({ isActive }) =>
              `nav-link ${isActive ? "active bg-primary" : "text-white link-hover"}`
            }
          >
            Profile
          </NavLink>
        </nav>
      </aside>
    </>
  );
}