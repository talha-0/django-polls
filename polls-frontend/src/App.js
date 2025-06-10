import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

import Login from './auth/Login';
import QuestionList from './pages/QuestionList';
import QuestionDetail from './pages/QuestionDetail';
import QuestionAdd from './pages/QuestionAdd';
import QuestionEdit from './pages/QuestionEdit';
import QuestionResults from './pages/QuestionResults';

import ChoiceList from './pages/ChoiceList';
import ChoiceAdd from './pages/ChoiceAdd';
import ChoiceEdit from './pages/ChoiceEdit';

import VoteList from './pages/VoteList';

const App = () => {
  const isAuthenticated = !!localStorage.getItem('access_token');

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* Questions */}
        <Route path="/questions" element={isAuthenticated ? <QuestionList /> : <Navigate to="/login" />} />
        <Route path="/questions/add" element={isAuthenticated ? <QuestionAdd /> : <Navigate to="/login" />} />
        <Route path="/questions/:id" element={isAuthenticated ? <QuestionDetail /> : <Navigate to="/login" />} />
        <Route path="/questions/:id/edit" element={isAuthenticated ? <QuestionEdit /> : <Navigate to="/login" />} />
        <Route path="/questions/:id/results" element={isAuthenticated ? <QuestionResults /> : <Navigate to="/login" />} />

        {/* Choices */}
        <Route path="/choices" element={isAuthenticated ? <ChoiceList /> : <Navigate to="/login" />} />
        <Route path="/choices/add" element={isAuthenticated ? <ChoiceAdd /> : <Navigate to="/login" />} />
        <Route path="/choices/:id/edit" element={isAuthenticated ? <ChoiceEdit /> : <Navigate to="/login" />} />

        {/* Votes */}
        <Route path="/votes" element={isAuthenticated ? <VoteList /> : <Navigate to="/login" />} />

        {/* Redirect */}
        <Route path="*" element={<Navigate to="/questions" />} />
      </Routes>
    </Router>
  );
};

export default App;
