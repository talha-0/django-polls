import React, { useEffect, useState } from 'react';
import Navbar from '../components/navbar';
import axios from '../api/axios';

export default function VoteList() {
  const [votes, setVotes] = useState([]);

  useEffect(() => {
    axios.get('votes/')
      .then(res => setVotes(res.data))
      .catch(() => alert('Failed to fetch votes'));
  }, []);

  return (
    <div>
      <Navbar />
      <h2>Votes</h2>
      <ul>
        {votes.map(vote => (
          <li key={vote.id}>
            User: {vote.voter.username} - Choice: {vote.choice} - Question: {vote.question}
          </li>
        ))}
      </ul>
    </div>
  );
}
