import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "../api/axios";
import Navbar from "../components/navbar";

export default function QuestionList() {
  const [questions, setQuestions] = useState([]);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);

  const fetchQuestions = (url = "questions/") => {
    axios
      .get(url)
      .then((res) => {
        setQuestions(res.data.results);
        setNextPage(res.data.next);
        setPrevPage(res.data.previous);
      })
      .catch(() => alert("Failed to fetch questions"));
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  const deleteQuestion = (id) => {
    if (!window.confirm("Delete this question?")) return;
    axios
      .delete(`questions/${id}/delete/`)
      .then(() => fetchQuestions())
      .catch(() => alert("Delete failed"));
  };

  return (
    <>
      <Navbar />
      <div className="bg-gray-900 py-20 px-4">
        <div className="max-w-4xl mx-auto bg-white/10 backdrop-blur-md rounded-xl shadow-xl p-6">
          <h2 className="text-3xl font-bold text-white mb-6 text-center">
            Questions
          </h2>
          {questions.length === 0 ? (
            <p className="text-gray-300 text-center">No questions available.</p>
          ) : (
            <>
              <ul className="space-y-4">
                {questions.map((q) => (
                  <li
                    key={q.id}
                    className="bg-white/10 hover:bg-white/20 transition-all duration-200 backdrop-blur-md text-white rounded-lg shadow-md p-4 flex flex-col md:flex-row md:justify-between md:items-center"
                  >
                    <span className="font-medium">{q.question_text}</span>
                    <div className="mt-2 md:mt-0 space-x-2 text-sm">
                      <Link
                        to={`/questions/${q.id}`}
                        className="inline-flex bg-blue-500 hover:bg-blue-600 text-white px-3 py-3 rounded-md"
                      >
                        View
                      </Link>
                      <Link
                        to={`/questions/${q.id}/edit`}
                        className="inline-flex bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-3 rounded-md"
                      >
                        Edit
                      </Link>
                      <Link
                        to={`/questions/${q.id}/edit`}
                        className="inline-flex bg-purple-500 hover:bg-purple-600 text-white px-3 py-3 rounded-md"
                      >
                        Results
                      </Link>
                      <button
                        onClick={() => deleteQuestion(q.id)}
                        className="inline-flex bg-red-500 hover:bg-red-600 text-white px-3 py-3 rounded-md"
                      >
                        Delete
                      </button>
                    </div>
                  </li>
                ))}
              </ul>

              <div className="flex justify-center mt-6 space-x-4">
                {prevPage && (
                  <button
                    onClick={() => fetchQuestions(prevPage)}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-md"
                  >
                    Previous
                  </button>
                )}
                {nextPage && (
                  <button
                    onClick={() => fetchQuestions(nextPage)}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-md"
                  >
                    Next
                  </button>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
}
