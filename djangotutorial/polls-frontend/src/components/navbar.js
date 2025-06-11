import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  };

  return (
    <div className="fixed w-full flex justify-center mt-4 z-50">
      <nav className="bg-white/10 backdrop-blur-md text-white shadow-lg rounded-full px-6 py-3 flex items-center gap-4">
        <Link to="/questions" className="hover:underline">
          Questions
        </Link>
        <Link to="/questions/add" className="hover:underline">
          Add Question
        </Link>
        <Link to="/choices" className="hover:underline">
          Choices
        </Link>
        <Link to="/choices/add" className="hover:underline">
          Add Choice
        </Link>
        <Link to="/votes" className="hover:underline">
          Votes
        </Link>
        <button
          onClick={handleLogout}
          className="ml-auto text-red-300 hover:text-red-500 transition-colors"
        >
          Logout
        </button>
      </nav>
    </div>
  );
}

export default Navbar;
