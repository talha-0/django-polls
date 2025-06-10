import React, { useEffect, useState } from 'react';
import Navbar from '../components/navbar';
import axios from '../api/axios';
import { Link } from 'react-router-dom';

export default function ChoiceList() {
  const [choices, setChoices] = useState([]);

  const fetchChoices = () => {
    axios.get('choices/')
      .then(res => setChoices(res.data))
      .catch(() => alert('Failed to fetch choices'));
  };

  useEffect(() => {
    fetchChoices();
  }, []);

  const deleteChoice = (id) => {
    if (!window.confirm('Delete this choice?')) return;
    axios.delete(`choices/${id}/delete/`)
      .then(() => fetchChoices())
      .catch(() => alert('Delete failed'));
  };

  return (
    <div>
      <Navbar />
      <h2>Choices</h2>
      <ul>
        {choices.map(choice => (
          <li key={choice.id}>
            {choice.choice_text} (Question ID: {choice.question})
            {" | "}
            <Link to={`/choices/${choice.id}/edit`}>Edit</Link>
            {" | "}
            <button onClick={() => deleteChoice(choice.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
