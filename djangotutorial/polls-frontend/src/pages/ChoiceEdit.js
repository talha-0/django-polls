import React, { useEffect, useState } from 'react';
import Navbar from '../components/navbar';
import axios from '../api/axios';
import { useParams, useNavigate } from 'react-router-dom';

export default function ChoiceEdit() {
  const { id } = useParams();
  const [choiceText, setChoiceText] = useState('');
  const [questionId, setQuestionId] = useState('');
  const [questions, setQuestions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`choices/${id}/`)
      .then(res => {
        setChoiceText(res.data.choice_text);
        setQuestionId(res.data.question);
      })
      .catch(() => alert('Failed to fetch choice'));
  }, [id]);

  useEffect(() => {
    axios.get('questions/')
      .then(res => setQuestions(res.data))
      .catch(() => alert('Failed to fetch questions'));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.put(`choices/${id}/update/`, { choice_text: choiceText, question: questionId })
      .then(() => navigate('/choices'))
      .catch(() => alert('Failed to update choice'));
  };

  return (
    <div>
      <Navbar />
      <h2>Edit Choice</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={choiceText}
          onChange={(e) => setChoiceText(e.target.value)}
          required
        />
        <select
          value={questionId}
          onChange={(e) => setQuestionId(e.target.value)}
          required
        >
          <option value="">Select question</option>
          {questions.map(q => (
            <option key={q.id} value={q.id}>{q.question_text}</option>
          ))}
        </select>
        <button type="submit">Update Choice</button>
      </form>
    </div>
  );
}
