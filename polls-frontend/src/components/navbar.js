import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  };

  return (
    <nav style={{ padding: "10px", background: "#eee", display: "flex", gap: "15px" }}>
      <Link to="/questions">Questions</Link>
      <Link to="/questions/add">Add Question</Link>
      <Link to="/choices">Choices</Link>
      <Link to="/choices/add">Add Choice</Link>
      <Link to="/votes">Votes</Link>
      <button onClick={handleLogout} style={{ marginLeft: "auto" }}>Logout</button>
    </nav>
  );
}

export default Navbar;
