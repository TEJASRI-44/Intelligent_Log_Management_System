import axios from "axios";

const BASE_URL = "http://localhost:8000";


function getAuthHeaders() {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}


export async function createUser(payload) {
  const res = await fetch(`${BASE_URL}/users/create`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

export async function getUsers() {
  const res = await fetch(`${BASE_URL}/users/view`, {
    headers: getAuthHeaders(),
  });

  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

export async function fetchRoles() {
  const res = await fetch(`${BASE_URL}/admin/roles`, {
    headers: getAuthHeaders(),
  });

  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

export async function fetchTeams() {
  const res = await fetch(`${BASE_URL}/admin/teams`, {
    headers: getAuthHeaders(),
  });

  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

export async function adminSearchLogs(filters) {
  const res = await axios.get(
    `${BASE_URL}/admin/logs/search`,
    {
      params: filters,
      headers: getAuthHeaders()
    }
  );
  return res.data;
}
export async function fetchAdminFiles(filters) {
  const res = await axios.get(`${BASE_URL}/admin/files`, {
    params: filters,
    headers: getAuthHeaders(),
  });
  return res.data;
}

export async function adminDeleteFile(fileId) {
  await axios.delete(`${BASE_URL}/admin/files/${fileId}`, {
    headers: getAuthHeaders(),
  });
}

export const adminRestoreFile = async (fileId) => {
  return axios.post(
    `http://localhost:8000/admin/files/${fileId}/restore`,
    {}, 
    {
      headers: getAuthHeaders(), 
    }
  );
};

export const adminDownloadFile = async (fileId) => {
  const res = await axios.get(
    `http://localhost:8000/admin/files/${fileId}/download`,
    {
      headers: getAuthHeaders(),
      responseType: "blob"
    }
  );

  const url = window.URL.createObjectURL(new Blob([res.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", "file");
  document.body.appendChild(link);
  link.click();
  link.remove();
};

export const runLogRetention = async () => {
  return axios.post(
    "http://localhost:8000/admin/retention/archive-now",
    {},
    { headers: getAuthHeaders() }
  );
};
