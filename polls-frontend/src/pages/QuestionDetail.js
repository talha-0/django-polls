import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "../api/axios";
import Navbar from "../components/navbar";

export default function QuestionDetail() {
  const { id } = useParams();
  const [question, setQuestion] = useState(null);
  const [choices, setChoices] = useState([]);
  const [voted, setVoted] = useState(false);

  useEffect(() => {
    axios.get(`questions/${id}/`).then((res) => setQuestion(res.data));
    axios.get(`choices/${id}/`).then((res) => setChoices(res.data));
  }, [id]);

  const vote = (choiceId) => {
    axios
      .post("vote/", { choice: choiceId })
      .then(() => setVoted(true))
      .catch((err) => alert(err.response?.data?.error || "Vote failed"));
  };

  if (!question) return <p>Loading...</p>;

  return (
    <div>
      <Navbar />
      <h3>{question.question_text}</h3>
      {voted ? (
        <>
          <p>You have voted.</p>
          <Link to={`/questions/${id}/results`}>View Results</Link>
          <br />
          <Link to="/questions">Back to Questions</Link>
        </>
      ) : (
        <>
          {choices.map((choice) => (
            <button key={choice.id} onClick={() => vote(choice.id)}>
              {choice.choice_text}
            </button>
          ))}
          <br />
          <Link to="/questions">Back to Questions</Link>
        </>
      )}
    </div>
  );
}
