import React, { useState, useRef } from 'react';
import { AudioRecorder } from '../utils/recorder';

const VoiceAssistant = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');
  
  const recorderRef = useRef(new AudioRecorder());

  // Use browser SpeechSynthesis for fast free voice output
  const speakResponse = (text) => {
    if (!window.speechSynthesis) {
      console.warn('Speech synthesis not supported in this browser.');
      return;
    }
    
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    // Optional: customize voice, pitch, rate here
    window.speechSynthesis.speak(utterance);
  };

  const handleStartRecording = async () => {
    setError('');
    const success = await recorderRef.current.startRecording();
    if (success) {
      setIsRecording(true);
    } else {
      setError('Could not access microphone. Please check permissions.');
    }
  };

  const handleStopRecording = async () => {
    setIsRecording(false);
    setIsProcessing(true);
    
    const audioBlob = await recorderRef.current.stopRecording();
    if (!audioBlob) {
      setIsProcessing(false);
      return;
    }

    // Prepare FormData
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');

    try {
      // Send directly to backend without permanent file storage
      const res = await fetch('http://localhost:8000/api/voice-chat', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Server returned an error');
      }

      const data = await res.json();
      setTranscript(data.transcript || '');
      setResponse(data.response || '');
      
      if (data.response) {
        speakResponse(data.response);
      }
    } catch (err) {
      console.error('Error during voice processing:', err);
      setError('Failed to process voice input. Is the backend running?');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="voice-assistant-container" style={{ padding: '20px', maxWidth: '600px', margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h2>Real-time Voice Assistant</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={isRecording ? handleStopRecording : handleStartRecording}
          disabled={isProcessing}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: isRecording ? '#ff4d4f' : '#4caf50',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          {isProcessing ? 'Processing...' : isRecording ? 'Stop Recording' : 'Start Recording'}
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
        <h4>You said:</h4>
        <p style={{ minHeight: '40px', fontStyle: 'italic' }}>{transcript || '...'}</p>
        
        <h4>Assistant reply:</h4>
        <p style={{ minHeight: '40px' }}>{response || '...'}</p>
      </div>
    </div>
  );
};

export default VoiceAssistant;
