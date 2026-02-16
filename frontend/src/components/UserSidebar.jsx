import { NavLink } from "react-router-dom";
import "../styles/UserSidebar.css";

export default function UserSidebar() {
  return (
     <>

      <button
        className="btn btn-dark d-md-none position-fixed top-0 start-0 m-3 z-3"
        onClick={() => setIsOpen(!isOpen)}
      >
       menu
      </button>
     
    <aside className="sidebar border-end position-fixed top-0 start-0 vh-100 vh-100 p-3 bg-dark " style={{ width: "220px" }}>
      
  
      <div className="mb-4  fw-bold fs-5  text-white"style={{ marginTop: "100px" }}>
        User Dashboard
      </div>

      
      <nav className="nav nav-pills flex-column gap-2 ">

        <NavLink
          to="/user/logs"
          className={({ isActive }) =>
            `nav-link ${isActive ? "active" : "text-white"}`
          }
        >
          Overview & Logs
        </NavLink>

        <NavLink
          to="/user/upload-file"
          className={({ isActive }) =>
            `nav-link ${isActive ? "active" : "text-white"}`
          }
        >
          Upload Files
        </NavLink>

        <NavLink
          to="/user/my-files"
          className={({ isActive }) =>
            `nav-link ${isActive ? "active" : "text-white"}`
          }
        >
          My Files
        </NavLink>

        <NavLink
          to="/user/profile"
          className={({ isActive }) =>
            `nav-link ${isActive ? "active" : "text-white"}`
          }
        >
          Profile
        </NavLink>

      </nav>
    </aside>
    </>
  );
}
