import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../auth/auth.api";
import { saveAuth } from "../auth/auth.service";
import "../styles/login.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const data = await login(email, password);
      console.log("LOGIN RESPONSE:", data);

      saveAuth(data.access_token, data.role);

      if (data.role === "ADMIN") {
        navigate("/admin");
      } else {
        navigate("/user");
      }
    } catch (err) {
      alert("Invalid credentials");
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <div className="login-container">
        <h2>Login</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button type="submit">Login</button>
      </div>
    </form>
  );
}
