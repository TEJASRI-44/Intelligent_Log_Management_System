import axios from "axios";
import { getToken } from "../auth/auth.service";

const API_URL = import.meta.env.VITE_API_URL||"http://localhost:8000/admin/reports";

function getAuthHeader() {
  const token = getToken();
  return {
    Authorization: `Bearer ${token}`
  };
}

export const fetchLogsPerDay = async () => {
  const res = await axios.get(`${API_URL}/logs-per-day`, {
    headers: getAuthHeader()
  });
  return res.data;
};

export const fetchTopErrors = async () => {
  const res = await axios.get(`${API_URL}/top-errors`, {
    headers: getAuthHeader()
  });
  return res.data;
};

export async function fetchActiveSystems(startDate, endDate) {
  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  const res = await fetch(
    `${API_URL}/active-systems?${params}`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    }
  );

  return res.json(); 
}

export async function fetchRecentLogs(days = 10, page = 1, limit = 10) {
  const res = await axios.get(
    `${API_URL}/recent-logs`,
    {
      params: { days, page, limit },
      headers: getAuthHeader()
    }
  );

  return res.data;
}
