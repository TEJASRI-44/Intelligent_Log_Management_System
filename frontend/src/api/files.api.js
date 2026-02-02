import axios from "axios";

const API_URL = "http://localhost:8000";

function getAuthHeader() {
  const token = localStorage.getItem("token");
  return {
    Authorization: `Bearer ${token}`
  };
}

export async function uploadLogFile(teamId, sourceId, formatId, file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post(
    `${API_URL}/files/upload`,
    formData,
    {
      params: {
        team_id: teamId,
        source_id: sourceId,
        format_id: formatId
      },
      headers: {
        ...getAuthHeader(),  
        "Content-Type": "multipart/form-data"
      }
    }
  );

  return res.data;
}
export async function fetchMyFiles(params = {}) {

  const cleanParams = Object.fromEntries(
    Object.entries(params).filter(
      ([_, v]) => v !== undefined && v !== null && v !== ""
    )
  );

  const query = new URLSearchParams(cleanParams).toString();

  const res = await fetch(
    `${API_URL}/users/files/my-files${query ? `?${query}` : ""}`,
    {
      headers: getAuthHeader()
    }
  );

  const data = await res.json();

  if (!res.ok) {
    console.error("fetchMyFiles failed:", data);
    throw new Error("Failed to fetch files");
  }

  return data; // { results, count }
}


export async function deleteMyFile(fileId) {
  await axios.delete(`http://localhost:8000/users/files/${fileId}`, {
    headers: getAuthHeader()
  });
}

export async function restoreMyFile(fileId) {
  await axios.patch(
    `${API_URL}/users/files/${fileId}/restore`,
    {},
    { headers: getAuthHeader() }
  );
}

export const userDownloadFile = async (fileId) => {
  const res = await axios.get(
    `http://localhost:8000/users/files/${fileId}/download`,
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