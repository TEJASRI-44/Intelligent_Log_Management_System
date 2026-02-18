import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL||"http://192.168.3.242:8000";

function getAuthHeader() {
  const token = localStorage.getItem("token");
  return {
    Authorization: `Bearer ${token}`
  };
}

export const fetchTeams = async () => {
  const res = await axios.get(`${API_URL}/teams`, {
    headers: getAuthHeader()
  });
  return res.data;
};

export const fetchSources = async () => {
  const res = await axios.get(`${API_URL}/log-sources`, {
    headers: getAuthHeader()
  });
  return res.data;
};

export const fetchFormats = async () => {
  const res = await axios.get(`${API_URL}/file-formats`, {
    headers: getAuthHeader()
  });
  return res.data;
};

export async function fetchMyTeams() {
  const res = await axios.get(
    `${API_URL}/users/my-teams`,
    { headers: getAuthHeader() }
  );
  return res.data;
}

export const fetchAllowedSources = (teamId) =>
  axios.get(`${API_URL}/lookups/team/${teamId}/sources`, {headers: getAuthHeader()})
    .then(res => res.data);

export const fetchAllowedFormats = (teamId, sourceId) =>
  axios.get(
    `${API_URL}/lookups/team/${teamId}/source/${sourceId}/formats`,
    {headers: getAuthHeader()}
  ).then(res => res.data);
