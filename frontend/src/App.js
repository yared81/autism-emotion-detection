import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import EmotionDetector from './components/EmotionDetector';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 mb-4">
            Emotion Detection AI
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Real-time facial emotion recognition powered by deep learning. 
            Detect emotions including Happy, Sad, Angry, Surprise, Fear, Disgust, and Neutral.
          </p>
        </header>
        
        <EmotionDetector apiUrl={API_URL} />
        
        <footer className="mt-16 text-center text-gray-500">
          <p>Powered by DeepFace & TensorFlow</p>
        </footer>
      </div>
    </div>
  );
}

export default App;

