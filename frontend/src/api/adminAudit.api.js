// src/api/adminAudit.api.js
import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL||"http://192.168.3.242:8000";

function authHeaders() {
  return {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  };
}

export async function fetchAuditLogs(page, limit, filters) {
  const res = await axios.get(`${BASE_URL}/admin/audits`, {
    params: {
      page,
      limit,
      ...filters
    },
    headers: authHeaders(),
  });
  return res.data;
}
