import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "../api/axios";
import Navbar from "../components/navbar";

export default function QuestionResults() {
  const { id } = useParams();
  const [results, setResults] = useState(null);

  useEffect(() => {
    axios
      .get(`questions/${id}/results/`)
      .then((res) => setResults(res.data))
      .catch(() => alert("Failed to fetch results"));
  }, [id]);

  if (!results) return <p>Loading results...</p>;

  return (
    <div>
      <Navbar />
      <h2>Results for Question {id}</h2>
      <ul>
        {results.results.map((choice, index) => (
          <li key={index}>
            {choice.choice_text} - Votes: {choice.votes}
          </li>
        ))}
      </ul>
    </div>
  );
}
