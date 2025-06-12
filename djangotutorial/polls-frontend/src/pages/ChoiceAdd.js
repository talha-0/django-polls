import React, { useState, useEffect } from "react";
import Navbar from "../components/navbar";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function ChoiceAdd() {
  const [choiceText, setChoiceText] = useState("");
  const [questionId, setQuestionId] = useState("");
  const [questions, setQuestions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get("questions/user/")
      .then((res) => setQuestions(res.data))
      .catch(() => alert("Failed to fetch questions"));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("choices/add/", { choice_text: choiceText, question: questionId })
      .then(() => navigate("/choices"))
      .catch(() => alert("Failed to add choice"));
  };

  return (
    <div>
      <Navbar />
      <h2>Add Choice</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={choiceText}
          onChange={(e) => setChoiceText(e.target.value)}
          placeholder="Choice text"
          required
        />
        <select
          value={questionId}
          onChange={(e) => setQuestionId(e.target.value)}
          required
        >
          <option value="">Select question</option>
          {questions.map((q) => (
            <option key={q.id} value={q.id}>
              {q.question_text}
            </option>
          ))}
        </select>
        <button type="submit">Add Choice</button>
      </form>
    </div>
  );
}
