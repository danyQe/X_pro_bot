import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import FactChecker from './pages/FactChecker';
import SentimentAnalyzer from './pages/SentimentAnalyzer';
import ViralGenerator from './pages/ViralGenerator';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/fact-checker" element={<FactChecker />} />
          <Route path="/sentiment" element={<SentimentAnalyzer />} />
          <Route path="/viral" element={<ViralGenerator />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;