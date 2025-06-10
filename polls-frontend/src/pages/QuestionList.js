import React, { useEffect, useState } from 'react';
import Navbar from '../components/navbar';
import axios from '../api/axios';
import { Link, useNavigate } from 'react-router-dom';

export default function QuestionList() {
  const [questions, setQuestions] = useState([]);
  const navigate = useNavigate();

  const fetchQuestions = () => {
    axios.get('questions/')
      .then(res => setQuestions(res.data))
      .catch(err => alert('Failed to fetch questions'));
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  const deleteQuestion = (id) => {
    if (!window.confirm('Delete this question?')) return;
    axios.delete(`questions/${id}/delete/`)
      .then(() => fetchQuestions())
      .catch(err => alert('Delete failed'));
  };

  return (
    <div>
      <Navbar />
      <h2>Questions</h2>
      <ul>
        {questions.map(q => (
          <li key={q.id} style={{ marginBottom: '10px' }}>
            <Link to={`/questions/${q.id}`}>{q.question_text}</Link>
            {" | "}
            <Link to={`/questions/${q.id}/edit`}>Edit</Link>
            {" | "}
            <Link to={`/questions/${q.id}/results`}>Results</Link>
            {" | "}
            <button onClick={() => deleteQuestion(q.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
