import axios from "axios";
import { getToken } from "../auth/auth.service";

const API_URL = import.meta.env.VITE_API_URL||"http://192.168.3.242:8000";

export const fetchUserStats = async () => {
  const res = await axios.get(`${API_URL}/users/stats/summary`, {
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  });
  return res.data;
};
