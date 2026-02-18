import axios from "axios";
import { getToken } from "../auth/auth.service";

const API_URL = import.meta.env.VITE_API_URL||"http://192.168.3.242:8000";

export const searchLogs = async (filters) => {
  const params = {};

  if (filters.start_date) params.start_date = filters.start_date;
  if (filters.end_date) params.end_date = filters.end_date;
  if (filters.category) params.category = filters.category;
  if (filters.severity) params.severity = filters.severity;
  if (filters.keyword) params.keyword = filters.keyword;

  const res = await axios.get(`${API_URL}/logs/search`, {
    params,
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  });

  return res.data;
};

export async function fetchMyLogs(filters = {}) {
  const cleanParams = Object.fromEntries(
    Object.entries(filters).filter(
      ([_, v]) => v !== undefined && v !== null && v !== ""
    )
  );

  const res = await axios.get(`${API_URL}/users/my-logs`, {
    params: cleanParams,
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  });

  return res.data;
}

