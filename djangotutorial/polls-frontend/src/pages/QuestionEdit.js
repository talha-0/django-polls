import React, { useEffect, useState } from 'react';
import Navbar from '../components/navbar';
import axios from '../api/axios';
import { useParams, useNavigate } from 'react-router-dom';

export default function QuestionEdit() {
  const { id } = useParams();
  const [questionText, setQuestionText] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`questions/${id}/`)
      .then(res => setQuestionText(res.data.question_text))
      .catch(() => alert('Failed to fetch question'));
  }, [id]);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.put(`questions/${id}/update/`, { question_text: questionText })
      .then(() => navigate('/questions'))
      .catch(() => alert('Failed to update question'));
  };

  return (
    <div>
      <Navbar />
      <h2>Edit Question</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={questionText}
          onChange={(e) => setQuestionText(e.target.value)}
          required
        />
        <button type="submit">Update</button>
      </form>
    </div>
  );
}
