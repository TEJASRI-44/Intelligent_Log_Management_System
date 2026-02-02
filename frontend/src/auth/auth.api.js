import axios from "axios";

const API_URL = "http://localhost:8000";

export const login = async (email, password) => {
  const res = await axios.post(`${API_URL}/users/login-json`, {
    email,
    password,
  });

  return res.data;
};
export function getCurrentUser() {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return {
      user_id: Number(payload.sub),
      email: payload.email,
      roles: payload.roles || []
    };
  } catch (e) {
    console.error("Invalid token");
    return null;
  }
}
export function getCurrentUserId() {
  const user = getCurrentUser();
  return user ? user.user_id : null;
}

export function getToken() {
  return localStorage.getItem("token");
}

export function logout() {
  localStorage.removeItem("token");
}