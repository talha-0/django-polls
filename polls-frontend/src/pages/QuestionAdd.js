import React, { useState } from 'react';
import Navbar from '../components/navbar';
import axios from '../api/axios';
import { useNavigate } from 'react-router-dom';

export default function QuestionAdd() {
  const [questionText, setQuestionText] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('questions/add/', { question_text: questionText })
      .then(() => navigate('/questions'))
      .catch(() => alert('Failed to add question'));
  };

  return (
    <div>
      <Navbar />
      <h2>Add Question</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={questionText}
          onChange={(e) => setQuestionText(e.target.value)}
          placeholder="Question text"
          required
        />
        <button type="submit">Add</button>
      </form>
    </div>
  );
}
