import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const EmotionDetector = ({ apiUrl }) => {
  const [isDetecting, setIsDetecting] = useState(false);
  const [emotion, setEmotion] = useState(null);
  const [emotions, setEmotions] = useState({});
  const [error, setError] = useState(null);
  const [fps, setFps] = useState(0);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const animationFrameRef = useRef(null);
  const lastFrameTimeRef = useRef(0);
  const frameCountRef = useRef(0);
  const isDetectingRef = useRef(false); // Use ref to track detection state for closures

  const emotionColors = {
    'happy': 'bg-green-500',
    'sad': 'bg-blue-500',
    'angry': 'bg-red-500',
    'surprised': 'bg-yellow-500',
    'surprise': 'bg-yellow-500', // fallback
    'fearful': 'bg-purple-500',
    'fear': 'bg-purple-500', // fallback
    'disgusted': 'bg-orange-500',
    'disgust': 'bg-orange-500', // fallback
    'neutral': 'bg-gray-500',
  };

  const emotionEmojis = {
    'happy': '😊',
    'sad': '😢',
    'angry': '😠',
    'surprised': '😲',
    'surprise': '😲', // fallback
    'fearful': '😨',
    'fear': '😨', // fallback
    'disgusted': '🤢',
    'disgust': '🤢', // fallback
    'neutral': '😐',
  };

  const startCamera = async () => {
    try {
      console.log('Requesting camera access...');
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        isDetectingRef.current = true; // Set ref immediately
        setIsDetecting(true);
        setError(null);
        
        // Wait for video to be ready before starting detection
        const handleVideoReady = () => {
          console.log('Video ready, starting detection...');
          if (isDetectingRef.current && videoRef.current && videoRef.current.readyState >= 2) {
            // Start detection loop
            detectEmotion();
          }
        };
        
        // Set up event listeners
        videoRef.current.onloadedmetadata = handleVideoReady;
        videoRef.current.onplaying = handleVideoReady;
        videoRef.current.oncanplay = handleVideoReady;
        
        // If video is already ready, start immediately
        if (videoRef.current.readyState >= 2) {
          console.log('Video already ready, starting immediately...');
          setTimeout(handleVideoReady, 100);
        }
        
        // Fallback: start detection after delay
        setTimeout(() => {
          if (isDetectingRef.current && videoRef.current && videoRef.current.readyState >= 2) {
            console.log('Starting detection (fallback)...');
            detectEmotion();
          }
        }, 1500);
      }
    } catch (err) {
      setError('Unable to access camera. Please check permissions.');
      console.error('Camera error:', err);
      isDetectingRef.current = false;
      setIsDetecting(false);
    }
  };

  const stopCamera = () => {
    console.log('Stopping camera...');
    isDetectingRef.current = false; // Stop detection immediately
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
    setIsDetecting(false);
    setEmotion(null);
    setEmotions({});
    setFps(0);
  };

  const detectEmotion = async () => {
    // Use ref to check detection state (avoids closure issues)
    if (!videoRef.current || !canvasRef.current || !isDetectingRef.current) {
      console.log('Detection stopped:', {
        video: !!videoRef.current,
        canvas: !!canvasRef.current,
        detecting: isDetectingRef.current
      });
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    // Check if video is ready
    if (video.readyState < video.HAVE_CURRENT_DATA) {
      // Video not ready yet, try again soon
      if (isDetectingRef.current) {
        setTimeout(detectEmotion, 100);
      }
      return;
    }
    
    // Check video dimensions
    if (video.videoWidth === 0 || video.videoHeight === 0) {
      if (isDetectingRef.current) {
        setTimeout(detectEmotion, 100);
      }
      return;
    }

    const ctx = canvas.getContext('2d');

    // Set canvas size to match video
    if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
    }

    // Draw video frame to canvas
    try {
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    } catch (err) {
      console.error('Error drawing video to canvas:', err);
      if (isDetectingRef.current) {
        setTimeout(detectEmotion, 100);
      }
      return;
    }

    // Convert canvas to base64
    const imageData = canvas.toDataURL('image/jpeg', 0.8);

    try {
      console.log('Sending detection request...');
      const response = await axios.post(`${apiUrl}/api/detect-emotion`, {
        image: imageData
      });
      console.log('Detection response received:', response.data);

      // Handle error response (e.g., no face detected) - don't throw, just show message
      if (response.data.error) {
        setError(response.data.error);
        setEmotion(null);
        setEmotions({});
        // Continue detection loop - user might move into frame
      } else {
        // Success - update emotion data
        setEmotion(response.data.dominant_emotion);
        setEmotions(response.data.emotions || {});
        setError(null);
      }

      // Calculate FPS
      const now = Date.now();
      frameCountRef.current++;
      if (now - lastFrameTimeRef.current >= 1000) {
        setFps(frameCountRef.current);
        frameCountRef.current = 0;
        lastFrameTimeRef.current = now;
      }
    } catch (err) {
      console.error('Detection error:', err);
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError('Failed to detect emotion. Please try again.');
      }
    } finally {
      // Always continue detection loop if camera is active
      // Use setTimeout to avoid blocking and ensure loop continues
      if (isDetectingRef.current) {
        setTimeout(() => {
          // Double-check before calling again (user might have stopped)
          if (isDetectingRef.current) {
            detectEmotion();
          }
        }, 300); // ~3-4 FPS to reduce load but ensure continuous detection
      }
    }
  };

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setError(null);
      const response = await axios.post(`${apiUrl}/api/detect-emotion-file`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.data.error) {
        throw new Error(response.data.error);
      }

      setEmotion(response.data.dominant_emotion);
      setEmotions(response.data.emotions || {});
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.response?.data?.error || 'Failed to detect emotion');
    }
  };

  const getEmotionColor = (emotionName) => {
    const key = emotionName?.toLowerCase();
    return emotionColors[key] || 'bg-gray-500';
  };

  const getEmotionEmoji = (emotionName) => {
    const key = emotionName?.toLowerCase();
    return emotionEmojis[key] || '😐';
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Video/Canvas Section */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="relative bg-black rounded-lg overflow-hidden aspect-video">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className={`w-full h-full object-cover ${isDetecting ? '' : 'hidden'}`}
            />
            <canvas
              ref={canvasRef}
              className="hidden"
            />
            {!isDetecting && (
              <div className="absolute inset-0 flex items-center justify-center text-gray-400">
                <div className="text-center">
                  <svg className="w-24 h-24 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  <p className="text-lg">Camera feed will appear here</p>
                </div>
              </div>
            )}
          </div>

          {/* Controls */}
          <div className="mt-6 flex flex-col sm:flex-row gap-4">
            {!isDetecting ? (
              <button
                onClick={startCamera}
                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                <span className="flex items-center justify-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  Start Camera
                </span>
              </button>
            ) : (
              <button
                onClick={stopCamera}
                className="flex-1 bg-red-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-red-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                <span className="flex items-center justify-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
                  </svg>
                  Stop Camera
                </span>
              </button>
            )}

            <label className="flex-1 bg-gradient-to-r from-green-600 to-teal-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-green-700 hover:to-teal-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 cursor-pointer text-center">
              <span className="flex items-center justify-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Upload Image
              </span>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                className="hidden"
              />
            </label>
          </div>

          {fps > 0 && (
            <div className="mt-4 text-sm text-gray-500 text-center">
              Processing: {fps} FPS
            </div>
          )}

          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Detection Results</h2>

          {emotion ? (
            <>
              {/* Dominant Emotion */}
              <div className="mb-6">
                <div className={`${getEmotionColor(emotion)} text-white rounded-xl p-6 text-center transform transition-all duration-300 hover:scale-105`}>
                  <div className="text-6xl mb-3">{getEmotionEmoji(emotion)}</div>
                  <div className="text-3xl font-bold capitalize">{emotion}</div>
                  {emotions[emotion] && (
                    <div className="text-lg mt-2 opacity-90">
                      {emotions[emotion].toFixed(1)}% confidence
                    </div>
                  )}
                </div>
              </div>

              {/* All Emotions */}
              <div className="space-y-3">
                <h3 className="text-lg font-semibold text-gray-700 mb-3">All Emotions</h3>
                {Object.entries(emotions)
                  .sort(([, a], [, b]) => b - a)
                  .map(([emotionName, confidence]) => (
                    <div key={emotionName} className="flex items-center gap-3">
                      <div className="flex-1">
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-sm font-medium text-gray-700 capitalize">
                            {emotionName}
                          </span>
                          <span className="text-sm text-gray-500">
                            {confidence.toFixed(1)}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                          <div
                            className={`${getEmotionColor(emotionName)} h-2.5 rounded-full transition-all duration-300`}
                            style={{ width: `${confidence}%` }}
                          />
                        </div>
                      </div>
                      <span className="text-2xl">{getEmotionEmoji(emotionName)}</span>
                    </div>
                  ))}
              </div>
            </>
          ) : (
            <div className="text-center py-12 text-gray-400">
              <svg className="w-24 h-24 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <p className="text-lg">Start camera or upload an image to detect emotions</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EmotionDetector;

