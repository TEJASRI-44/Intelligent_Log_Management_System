import axios from "axios";
import { getToken } from "../auth/auth.service";
/* import { API } from "./axios_api"; */
const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

const authHeader = () => ({
  Authorization: `Bearer ${getToken()}`
});


export const fetchUsers = async ({
  email,
  team_id,
  page = 1,
  limit = 10
} = {}) => {
  const res = await axios.get(`${API}/admin/users`, {
    headers: authHeader(),
    params: {
      email,
      team_id,
      page,
      limit
    }
  });

  return res.data;
};

export const updateUserStatus = async (userId, isActive) => {
  await axios.patch(
    `${API}/admin/users/${userId}/status`,
    { is_active: isActive },
    { headers: authHeader() }
  );
};

export const deleteUser = async (userId) => {
  await axios.delete(`${API}/admin/users/${userId}`, {
    headers: authHeader()
  });
};

export const updateUserProfile = (userId, payload) =>
  axios.put(`${API}/admin/users/${userId}/profile`, payload, {
    headers: authHeader()
  });

export const updateUserAccess = (userId, roleIds, teamIds) =>
  axios.put(
    `${API}/admin/users/${userId}/access`,
    {
      role_ids: roleIds,
      team_ids: teamIds
    },
    { headers: authHeader() }
  );
