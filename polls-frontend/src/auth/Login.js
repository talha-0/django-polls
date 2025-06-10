import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";

export default function Login() {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });
  const navigate = useNavigate();

  const login = async (e) => {
    e.preventDefault();
    try {
      const { data } = await axios.post("/token/", credentials);
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      navigate("/questions");
    } catch (err) {
      alert(err);
      alert("Invalid login");
    }
  };

  return (
    <form onSubmit={login}>
      <input
        type="text"
        placeholder="Username"
        onChange={(e) =>
          setCredentials({ ...credentials, username: e.target.value })
        }
      />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) =>
          setCredentials({ ...credentials, password: e.target.value })
        }
      />
      <button type="submit">Login</button>
    </form>
  );
}
