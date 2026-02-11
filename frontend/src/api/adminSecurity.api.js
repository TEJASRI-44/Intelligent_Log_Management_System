// src/api/adminSecurity.api.js
import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL||"http://localhost:8000";

function authHeaders() {
  return {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  };
}

export async function fetchLoginHistory(page, limit, success) {
  const res = await axios.get(
    `${BASE_URL}/admin/security/login-history`,
    {
      params: { page, limit, success },
      headers: authHeaders(),
    }
  );
  return res.data;
}
