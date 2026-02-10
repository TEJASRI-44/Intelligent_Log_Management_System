// src/pages/user/UserSearchLogs.jsx
import { useEffect, useState } from "react";
import { fetchMyLogs, searchLogs } from "../api/logs.api";
import { fetchUserStats } from "../api/stats.api";
import "../styles/UserSearchLogs.css";
import "bootstrap/dist/css/bootstrap.min.css";
export default function UserSearchLogs() {
  const [userStats, setUserStats] = useState(null);
  const [userLogs, setUserLogs] = useState([]);
  const [userFilters, setUserFilters] = useState({
    start_date: "",
    end_date: "",
    category: "",
    severity: "",
    keyword: ""
  });
  const [userPage, setUserPage] = useState(1);
  const [userPageSize, setUserPageSize] = useState(10);
  const [userTotalLogs, setUserTotalLogs] = useState(0);
  const [userLogScope, setUserLogScope] = useState("MY");
  const [userSearchMsg, setUserSearchMsg] = useState("");

  /* ================= EFFECTS ================= */

  useEffect(() => {
    fetchUserStats().then(setUserStats);
  }, []);

  useEffect(() => {
  loadUserLogs();
}, [userPage, userPageSize, userLogScope, userFilters]);


  /* ================= HANDLERS ================= */

  async function loadUserLogs(filters = userFilters) {
  setUserLogs([]);
  setUserSearchMsg("");

  try {
    let res;

    if (userLogScope === "MY") {
      res = await fetchMyLogs({
        ...filters,
        page: userPage,
        limit: userPageSize
      });
    } else {
      res = await searchLogs({
        ...filters,
        page: userPage,
        limit: userPageSize,
        scope: userLogScope
      });
    }

    setUserLogs(res.results || []);
    setUserTotalLogs(res.count || 0);
    setUserSearchMsg(`Found ${res.count} log entries`);
  } catch {
    setUserSearchMsg("Failed to fetch logs");
  }
}

function handleUserSearch(e) {
  e.preventDefault();
  setUserPage(1); 
}



function resetFilters() {
  setUserFilters({
    start_date: "",
    end_date: "",
    category: "",
    severity: "",
    keyword: ""
  });
  setUserPage(1);
}




  /* ================= RENDER ================= */

  return (
    <div className="user-page-content">
      <div className="user-page-header">
        <h1>Search Logs</h1>
        <p>Search and filter through your system logs</p>
      </div>

      {/* ===== STATS ===== */}
      {userStats && (
        <div className="user-stats-grid">
          <div className="user-stat-card">
            <h3>{userStats.files_uploaded}</h3>
            <p>Files Uploaded</p>
          </div>

          <div className="user-stat-card">
            <h3>{userStats.total_logs}</h3>
            <p>Total Logs</p>
          </div>

          <div className="user-stat-card error">
            <h3>{userStats.error_logs}</h3>
            <p>Error Logs</p>
          </div>

          <div className="user-stat-card warning">
            <h3>{userStats.warning_logs}</h3>
            <p>Warning Logs</p>
          </div>
        </div>
      )}

      {/* ===== FILTER ===== */}
      <div className="user-card">
        <div className="user-card-header">
          <h2>Filter Logs</h2>
        </div>

        <form className="user-search-form " onSubmit={handleUserSearch}>
          <input
            placeholder="Search by keyword..."
            value={userFilters.keyword}
            onChange={e =>
              setUserFilters({ ...userFilters, keyword: e.target.value })
            }
          />

          <select
            value={userFilters.category}
            onChange={e =>
              setUserFilters({ ...userFilters, category: e.target.value })
            }
          >
            <option value="">All Categories</option>
            <option>APPLICATION</option>
            <option>SECURITY</option>
            <option>INFRASTRUCTURE</option>
            <option>AUDIT</option>
          </select>

          <select
            value={userFilters.severity}
            onChange={e =>
              setUserFilters({ ...userFilters, severity: e.target.value })
            }
          >
            <option value="">All Severities</option>
            <option>INFO</option>
            <option>WARN</option>
            <option>ERROR</option>
            <option>FATAL</option>
          </select>

          <input
            type="date"
            value={userFilters.start_date}
            onChange={e =>
              setUserFilters({ ...userFilters, start_date: e.target.value })
            }
          />

          <input
            type="date"
            value={userFilters.end_date}
            onChange={e =>
              setUserFilters({ ...userFilters, end_date: e.target.value })
            }
          />
            
              <select
               
                value={userLogScope}
                onChange={e => setUserLogScope(e.target.value)}
              >
                <option value="MY">My Logs</option>
                <option value="TEAM">My Team Logs</option>
                <option value="ALL">All Logs</option>
              </select>
         
            <div className="d-flex">
            
              <div>
                
                <select
               
                value={userPageSize}
                onChange={e => setUserPageSize(Number(e.target.value))}
              >
                <option value={10}>10</option>
                <option value={25}>25</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
              </select>

              <label htmlFor="logs per page" className="m-3">Rows</label>
              </div>
               
            </div>
            
         
            <div className="d-flex h-75 align-items-center flex-row justify-content-around ">

               {/*  <button type="submit" className="col-md-4 mx-2 user-primary-btn rounded-2 search">
                    Search 
                </button> */}
                <button type="button" className="col-md-6 mx-2 user-secondary-btn rounded-2 reset" onClick={resetFilters}>
                    Reset 
                </button>
            </div>
        </form>
      </div>

      {/* ===== MESSAGE ===== */}
      {userSearchMsg && (
        <div className="user-alert">
          {userSearchMsg}
        </div>
      )}

      {/* ===== RESULTS ===== */}
      {userLogs.length > 0 && (
        <div className="user-card">
          <div className="user-card-header">
            <h2>Search Results</h2>
          </div>

          <div className="user-table-container">
            <table className="user-data-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Severity</th>
                  <th>Service</th>
                  <th>Message</th>
                </tr>
              </thead>
              <tbody>
                {userLogs.map((log, i) => (
                  <tr key={i}>
                    <td>{new Date(log.timestamp).toLocaleString()}</td>
                    <td>
                      <span className={`user-badge ${log.severity.toLowerCase()}`}>
                        {log.severity}
                      </span>
                    </td>
                    <td>{log.service || "-"}</td>
                    <td className="user-message-cell">{log.message}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            {userTotalLogs > userPageSize && (
              <div className="user-pagination">
                <button
                  type="button"
                  disabled={userPage === 1}
                  onClick={() => setUserPage(p => p - 1)}
                >
                  Prev
                </button>

                <span>
                  Page {userPage} of {Math.ceil(userTotalLogs / userPageSize)}
                </span>

                <button
                  type="button"
                  disabled={userPage >= Math.ceil(userTotalLogs / userPageSize)}
                  onClick={() => setUserPage(p => p + 1)}
                >
                  Next
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
