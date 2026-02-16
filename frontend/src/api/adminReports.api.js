import axios from "axios";
import { getToken } from "../auth/auth.service";

const BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";


function getAuthHeader() {
  const token = getToken();
  return {
    Authorization: `Bearer ${token}`
  };
}

export const fetchLogsPerDay = async () => {
  const res = await axios.get(`${BASE_URL}/admin/reports/logs-per-day`, {
    headers: getAuthHeader()
  });
  return res.data;
};

export const fetchTopErrors = async () => {
  const res = await axios.get(`${BASE_URL}/admin/reports/top-errors`, {
    headers: getAuthHeader()
  });
  return res.data;
};

export async function fetchActiveSystems(startDate, endDate) {
  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  const res = await fetch(
    `${BASE_URL}/admin/reports/active-systems?${params}`,
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
    `${BASE_URL}/admin/reports/recent-logs`,
    {
      params: { days, page, limit },
      headers: getAuthHeader()
    }
  );

  return res.data;
}
