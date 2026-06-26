import React, { useRef } from 'react';
import EmotionDetector from './components/EmotionDetector';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

/* ─── Icon Components ──────────────────────────────────── */
const IconBrain = () => (
  <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z" />
    <path strokeLinecap="round" strokeLinejoin="round" d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z" />
  </svg>
);

const IconCamera = () => (
  <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
  </svg>
);

const IconActivity = () => (
  <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <polyline strokeLinecap="round" strokeLinejoin="round" points="22 12 18 12 15 21 9 3 6 12 2 12" />
  </svg>
);

const IconShield = () => (
  <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
  </svg>
);

const IconArrowDown = () => (
  <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 5v14m0 0l-7-7m7 7l7-7" />
  </svg>
);

const IconGitHub = () => (
  <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24">
    <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
  </svg>
);

/* ─── Feature Card ─────────────────────────────────────── */
const FeatureCard = ({ icon, title, desc }) => (
  <div className="feature-card">
    <div className="feature-icon">{icon}</div>
    <h3 className="feature-title">{title}</h3>
    <p className="feature-desc">{desc}</p>
  </div>
);

/* ─── Stat Block ───────────────────────────────────────── */
const Stat = ({ value, label }) => (
  <div className="stat-block">
    <span className="stat-value">{value}</span>
    <span className="stat-label">{label}</span>
  </div>
);

/* ─── Main App ─────────────────────────────────────────── */
function App() {
  const toolRef = useRef(null);

  const scrollToTool = () => {
    toolRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="app-root">

      {/* ── Navbar ─────────────────────────────────────── */}
      <header className="navbar">
        <div className="nav-inner">
          <a href="/" className="nav-logo">
            <span className="logo-dot" />
            EmoDetect
          </a>
          <nav className="nav-links">
            <a href="#about">About</a>
            <a href="#tool" onClick={(e) => { e.preventDefault(); scrollToTool(); }}>Try It</a>
            <a
              href="https://github.com/yared81/autism-emotion-detection"
              target="_blank"
              rel="noopener noreferrer"
              className="nav-github"
            >
              <IconGitHub />
              GitHub
            </a>
          </nav>
        </div>
      </header>

      {/* ── Hero ───────────────────────────────────────── */}
      <section className="hero" id="about">
        <div className="hero-badge">
          <span className="badge-dot" />
          Research Project · Facial Expression Analysis
        </div>

        <h1 className="hero-title">
          Real-Time Emotion
          <br />
          Recognition
        </h1>

        <p className="hero-sub">
          A computer vision tool that detects facial expressions from a live
          camera feed. Built to support research in behavioral and developmental
          psychology — specifically around autism spectrum disorder.
        </p>

        <div className="hero-actions">
          <button className="btn-primary" onClick={scrollToTool}>
            Launch Tool
            <IconCamera />
          </button>
          <a
            href="https://github.com/yared81/autism-emotion-detection"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-ghost"
          >
            <IconGitHub />
            View Source
          </a>
        </div>

        <div className="hero-stats">
          <Stat value="7" label="Emotion Classes" />
          <div className="stat-sep" />
          <Stat value="CNN" label="Model Architecture" />
          <div className="stat-sep" />
          <Stat value="Real-Time" label="Processing" />
          <div className="stat-sep" />
          <Stat value="Local" label="Privacy First" />
        </div>

        <button className="scroll-hint" onClick={scrollToTool} aria-label="Scroll to tool">
          <IconArrowDown />
        </button>
      </section>

      {/* ── Features ───────────────────────────────────── */}
      <section className="features-section">
        <div className="section-inner">
          <p className="section-label">How It Works</p>
          <h2 className="section-title">Snapshot. Analyze. Understand.</h2>
          <div className="features-grid">
            <FeatureCard
              icon={<IconCamera />}
              title="Webcam Capture"
              desc="Activate your device camera and take a single-frame snapshot directly in the browser — no installation required."
            />
            <FeatureCard
              icon={<IconBrain />}
              title="CNN Inference"
              desc="Your snapshot is analyzed by a convolutional neural network trained on labeled facial expression datasets."
            />
            <FeatureCard
              icon={<IconActivity />}
              title="Emotion Breakdown"
              desc="Receive a ranked breakdown of seven detected emotion classes — happy, sad, angry, fearful, disgusted, surprised, and neutral."
            />
            <FeatureCard
              icon={<IconShield />}
              title="Privacy Preserved"
              desc="Images are processed locally and never stored. The tool is designed for controlled research environments."
            />
          </div>
        </div>
      </section>

      {/* ── Detector Tool ──────────────────────────────── */}
      <section className="tool-section" id="tool" ref={toolRef}>
        <div className="section-inner">
          <p className="section-label">Live Demo</p>
          <h2 className="section-title">Try the Detector</h2>
          <p className="section-sub">
            Grant camera access, position your face in frame, and tap{' '}
            <span className="inline-code">Snapshot</span> to run analysis.
          </p>
          <EmotionDetector apiUrl={API_URL} />
        </div>
      </section>

      {/* ── Footer ─────────────────────────────────────── */}
      <footer className="footer">
        <div className="footer-inner">
          <span className="footer-logo">EmoDetect</span>
          <span className="footer-copy">
            Research project · Built with React &amp; Python · Not for clinical use
          </span>
          <a
            href="https://github.com/yared81/autism-emotion-detection"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-github"
          >
            <IconGitHub />
          </a>
        </div>
      </footer>
    </div>
  );
}

export default App;
