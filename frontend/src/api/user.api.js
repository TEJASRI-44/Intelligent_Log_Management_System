import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL||"http://localhost:8000";

function authHeader() {
  const token = localStorage.getItem("token");
  return {
    Authorization: `Bearer ${token}`
  };
}

/* 🔹 FETCH PROFILE */
export const fetchMyProfile = async () => {
  const res = await axios.get(
    `${API_URL}/users/me`,
    { headers: authHeader() }
  );
  return res.data;
};

/* 🔹 UPDATE PROFILE */
export const updateMyProfile = async (payload) => {
  const res = await axios.put(
    `${API_URL}/users/me`,
    payload,
    { headers: authHeader() }
  );
  return res.data;
};

export const changeMyPassword = async (payload) =>{
    const res = await axios.put(
    `${API_URL}/users/me/password`, 
    payload, 
    { headers: authHeader()}); 
      return res.data;
 };
