import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './EmotionDetector.css';

/* ─── Emotion Config ────────────────────────────────────── */
const EMOTION_META = {
  happy:     { label: 'Happy',     color: '#22c55e', icon: '😊' },
  sad:       { label: 'Sad',       color: '#60a5fa', icon: '😢' },
  angry:     { label: 'Angry',     color: '#ef4444', icon: '😠' },
  fearful:   { label: 'Fearful',   color: '#a78bfa', icon: '😨' },
  disgusted: { label: 'Disgusted', color: '#f97316', icon: '🤢' },
  surprised: { label: 'Surprised', color: '#fbbf24', icon: '😲' },
  neutral:   { label: 'Neutral',   color: '#6b7280', icon: '😐' },
};

/* ─── Inline SVG Icons ──────────────────────────────────── */
const IconCamera = ({ size = 16 }) => (
  <svg width={size} height={size} fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
  </svg>
);

const IconAperture = ({ size = 16 }) => (
  <svg width={size} height={size} fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="10" />
    <line x1="14.31" y1="8" x2="20.05" y2="17.94" strokeLinecap="round" />
    <line x1="9.69" y1="8" x2="21.17" y2="8" strokeLinecap="round" />
    <line x1="7.38" y1="12" x2="13.12" y2="2.06" strokeLinecap="round" />
    <line x1="9.69" y1="16" x2="3.95" y2="6.06" strokeLinecap="round" />
    <line x1="14.31" y1="16" x2="2.83" y2="16" strokeLinecap="round" />
    <line x1="16.62" y1="12" x2="10.88" y2="21.94" strokeLinecap="round" />
  </svg>
);

const IconStop = ({ size = 16 }) => (
  <svg width={size} height={size} fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <rect x="6" y="6" width="12" height="12" rx="1" />
  </svg>
);

const IconRefresh = ({ size = 16 }) => (
  <svg width={size} height={size} fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
  </svg>
);

const IconVideoOff = ({ size = 32 }) => (
  <svg width={size} height={size} fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2zM3 3l18 18" />
  </svg>
);

const IconAlert = ({ size = 15 }) => (
  <svg width={size} height={size} fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
  </svg>
);

/* ─── Spinner ───────────────────────────────────────────── */
const Spinner = () => (
  <div className="ed-spinner" role="status" aria-label="Analyzing...">
    <div className="ed-spinner-ring" />
  </div>
);

/* ─── Main Component ────────────────────────────────────── */
const EmotionDetector = ({ apiUrl }) => {
  const [isCameraOn, setIsCameraOn]   = useState(false);
  const [emotion, setEmotion]         = useState(null);
  const [emotions, setEmotions]       = useState({});
  const [error, setError]             = useState(null);
  const [loading, setLoading]         = useState(false);
  const [snapshot, setSnapshot]       = useState(null);
  const [cameraReady, setCameraReady] = useState(false);

  const videoRef  = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  /* Start camera */
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' },
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsCameraOn(true);
        setError(null);
        setSnapshot(null);
        setEmotion(null);
        setEmotions({});
        setCameraReady(false);
      }
    } catch {
      setError('Camera access denied. Please allow camera permissions and try again.');
    }
  };

  /* Stop camera */
  const stopCamera = () => {
    streamRef.current?.getTracks().forEach(t => t.stop());
    streamRef.current = null;
    setIsCameraOn(false);
    setCameraReady(false);
  };

  /* Capture snapshot & call API */
  const takeSnapshot = async () => {
    if (!videoRef.current || !canvasRef.current) return;
    const video  = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width  = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const imageData = canvas.toDataURL('image/jpeg', 0.9);

    setSnapshot(imageData);
    setLoading(true);
    setError(null);

    try {
      const { data } = await axios.post(`${apiUrl}/api/detect-emotion`, { image: imageData });
      if (data.error) {
        setError(data.error);
        setEmotion(null);
        setEmotions({});
      } else {
        setEmotion(data.dominant_emotion);
        setEmotions(data.emotions || {});
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Detection failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  /* Retake */
  const retake = () => {
    setSnapshot(null);
    setEmotion(null);
    setEmotions({});
    setError(null);
  };

  /* Cleanup on unmount */
  useEffect(() => { return () => stopCamera(); }, []);

  const sorted     = Object.entries(emotions).sort(([, a], [, b]) => b - a);
  const meta       = emotion ? (EMOTION_META[emotion.toLowerCase()] || {}) : {};
  const topScore   = emotions[emotion] ?? 0;

  return (
    <div className="ed-root">

      {/* ── Left: Camera Panel ─────────────────────────── */}
      <div className="ed-camera-panel">

        {/* Viewport */}
        <div className="ed-viewport">
          {/* Live feed */}
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            onCanPlay={() => setCameraReady(true)}
            className={`ed-video ${isCameraOn && !snapshot ? 'ed-visible' : ''}`}
          />

          {/* Snapshot preview */}
          {snapshot && (
            <img src={snapshot} alt="Captured frame" className="ed-snapshot" />
          )}

          {/* Idle state */}
          {!isCameraOn && !snapshot && (
            <div className="ed-idle">
              <div className="ed-idle-icon">
                <IconVideoOff size={28} />
              </div>
              <p className="ed-idle-title">Camera inactive</p>
              <p className="ed-idle-sub">Tap "Start Camera" to begin</p>
            </div>
          )}

          {/* Corner grid lines — scanner aesthetic */}
          {isCameraOn && cameraReady && !snapshot && (
            <div className="ed-scanner-overlay" aria-hidden="true">
              <div className="ed-corner tl" />
              <div className="ed-corner tr" />
              <div className="ed-corner bl" />
              <div className="ed-corner br" />
            </div>
          )}

          {/* Loading overlay */}
          {loading && (
            <div className="ed-loading-overlay">
              <Spinner />
              <span className="ed-loading-text">Analyzing frame…</span>
            </div>
          )}

          {/* Live indicator */}
          {isCameraOn && !snapshot && cameraReady && (
            <div className="ed-live-badge">
              <span className="ed-live-dot" />
              LIVE
            </div>
          )}

          {/* Dominant emotion badge on snapshot */}
          {snapshot && emotion && !loading && (
            <div className="ed-result-badge" style={{ '--accent-color': meta.color }}>
              <span className="ed-result-icon">{meta.icon}</span>
              <span className="ed-result-label">{meta.label || emotion}</span>
              <span className="ed-result-score">{topScore.toFixed(1)}%</span>
            </div>
          )}

          <canvas ref={canvasRef} className="ed-canvas" aria-hidden="true" />
        </div>

        {/* Controls */}
        <div className="ed-controls">
          {!isCameraOn ? (
            <button id="btn-start-camera" className="ed-btn ed-btn-primary" onClick={startCamera}>
              <IconCamera size={15} />
              Start Camera
            </button>
          ) : (
            <>
              <button
                id="btn-snapshot"
                className="ed-btn ed-btn-primary"
                onClick={takeSnapshot}
                disabled={loading || !cameraReady}
              >
                <IconAperture size={15} />
                Snapshot
              </button>
              <button
                id="btn-stop-camera"
                className="ed-btn ed-btn-ghost"
                onClick={stopCamera}
                disabled={loading}
              >
                <IconStop size={15} />
                Stop
              </button>
              {snapshot && (
                <button
                  id="btn-retake"
                  className="ed-btn ed-btn-ghost ed-btn-ml"
                  onClick={retake}
                  disabled={loading}
                >
                  <IconRefresh size={15} />
                  Retake
                </button>
              )}
            </>
          )}
        </div>

        {/* Error */}
        {error && (
          <div className="ed-error" role="alert">
            <IconAlert />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* ── Right: Results Panel ───────────────────────── */}
      <div className="ed-results-panel">
        <div className="ed-results-header">
          <span className="ed-results-label">Analysis Results</span>
          {emotion && !loading && (
            <span className="ed-results-status ed-results-status--ok">
              <span className="ed-status-dot" />
              Complete
            </span>
          )}
          {!emotion && !loading && (
            <span className="ed-results-status">
              Awaiting snapshot
            </span>
          )}
          {loading && (
            <span className="ed-results-status">
              Processing…
            </span>
          )}
        </div>

        {/* Placeholder state */}
        {!emotion && !loading && (
          <div className="ed-results-empty">
            <div className="ed-empty-rows">
              {Array.from({ length: 7 }).map((_, i) => (
                <div key={i} className="ed-empty-row">
                  <div className="ed-skel ed-skel-label" />
                  <div className="ed-skel ed-skel-bar" style={{ width: `${30 + Math.random() * 50}%` }} />
                  <div className="ed-skel ed-skel-score" />
                </div>
              ))}
            </div>
            <p className="ed-empty-hint">Emotion scores will appear here after analysis</p>
          </div>
        )}

        {/* Results bars */}
        {emotion && !loading && (
          <div className="ed-bars">
            {sorted.map(([name, score]) => {
              const m          = EMOTION_META[name.toLowerCase()] || {};
              const isDominant = name.toLowerCase() === emotion.toLowerCase();
              return (
                <div key={name} className={`ed-bar-row ${isDominant ? 'ed-bar-row--top' : ''}`}>
                  <div className="ed-bar-meta">
                    <span className="ed-bar-icon">{m.icon || '•'}</span>
                    <span className="ed-bar-name">{m.label || name}</span>
                    {isDominant && <span className="ed-bar-dominant-tag">dominant</span>}
                  </div>
                  <div className="ed-bar-track">
                    <div
                      className="ed-bar-fill"
                      style={{
                        width: `${score}%`,
                        background: m.color || 'var(--accent)',
                      }}
                    />
                  </div>
                  <span className="ed-bar-score">{score.toFixed(1)}%</span>
                </div>
              );
            })}
          </div>
        )}

        {/* Technical note */}
        <div className="ed-tech-note">
          <span className="ed-tech-label">Model</span>
          <span className="ed-tech-value">CNN · FER-2013</span>
          <span className="ed-tech-label">Backend</span>
          <span className="ed-tech-value">Python / Flask</span>
          <span className="ed-tech-label">Privacy</span>
          <span className="ed-tech-value">Local inference only</span>
        </div>
      </div>

    </div>
  );
};

export default EmotionDetector;
