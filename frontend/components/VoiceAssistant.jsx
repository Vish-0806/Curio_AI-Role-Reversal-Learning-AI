"use client";

import React, { useState, useRef } from 'react';
import { Mic, Square, Volume2, AudioLines, Zap } from 'lucide-react';
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
    <div className="w-full max-w-2xl mx-auto font-outfit">
      <div className="relative overflow-hidden rounded-[3rem] bg-white dark:bg-[#020617]/80 backdrop-blur-2xl shadow-[0_20px_50px_rgba(0,0,0,0.1)] dark:shadow-blue-900/20 border border-slate-200 dark:border-white/10 p-10 animate-fade-in-up">
        
        {/* Decorative ambient background */}
        <div className="absolute top-0 left-0 right-0 h-40 bg-gradient-to-b from-blue-600 to-transparent opacity-5 dark:opacity-10 pointer-events-none"></div>

        <div className="relative flex flex-col items-center text-center">
          <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-[2.5rem] bg-slate-900 dark:bg-blue-600 text-white shadow-xl shadow-slate-200 dark:shadow-blue-900/40">
            <Volume2 size={36} className="fill-current" />
          </div>
          
          <h2 className="text-4xl font-black text-slate-900 dark:text-white tracking-tighter mb-2">
            Vocal <span className="text-blue-600">Interface</span>
          </h2>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-10 max-w-md">
            Communicate hands-free. Curio AI will listen and respond dynamically via audio synthesis.
          </p>
          
          <div className="mb-10 w-full relative group">
             {/* Decorative Glow */}
             <div className={`absolute -inset-1 rounded-[3rem] blur-md transition duration-500 pointer-events-none ${isRecording ? 'bg-rose-500/30 opacity-100 animate-pulse' : 'bg-blue-500/30 opacity-0 group-hover:opacity-100'}`}></div>

            <button 
              onClick={isRecording ? handleStopRecording : handleStartRecording}
              disabled={isProcessing}
              className={`relative w-full flex items-center justify-center gap-4 px-12 py-7 rounded-[2.5rem] font-black text-xl transition-all shadow-2xl active:scale-95 tracking-tighter ${
                isProcessing 
                  ? 'bg-slate-200 dark:bg-slate-800 text-slate-500 cursor-not-allowed border dark:border-white/5'
                  : isRecording 
                    ? 'bg-rose-600 text-white shadow-rose-600/30 hover:bg-rose-500 hover:scale-105' 
                    : 'bg-slate-900 text-white shadow-slate-900/20 hover:bg-slate-800 hover:scale-105 dark:bg-blue-600 dark:shadow-blue-600/30 dark:hover:bg-blue-500'
              }`}
            >
              {isProcessing ? (
                <>
                  <div className="h-5 w-5 animate-spin rounded-full border-2 border-slate-400 border-t-white" />
                  PROCESSING AUDIO...
                </>
              ) : isRecording ? (
                <>
                  <Square size={22} className="fill-current" />
                  STOP RECORDING
                </>
              ) : (
                <>
                  <Mic size={22} className="fill-current" />
                  INITIALIZE MICROPHONE
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="mb-6 rounded-[2rem] bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 p-4 w-full">
              <p className="text-sm font-bold text-rose-600 dark:text-rose-400 tracking-tight">{error}</p>
            </div>
          )}

          <div className="w-full space-y-6">
            <div className="relative w-full rounded-[2.5rem] border border-slate-100 dark:border-white/5 bg-slate-50/50 dark:bg-white/5 backdrop-blur-md p-6 text-left">
              <div className="mb-3 flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-slate-200/50 dark:bg-slate-800 text-slate-500 dark:text-slate-400">
                   <Mic size={14} />
                </div>
                <h4 className="text-[11px] font-black uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500">
                  Transcribed Audio
                </h4>
              </div>
              <p className={`min-h-[60px] text-sm font-medium leading-relaxed ${transcript ? 'text-slate-800 dark:text-slate-200' : 'text-slate-400 dark:text-slate-600 italic'}`}>
                {transcript || 'Awaiting audio input...'}
              </p>
            </div>

            <div className="relative w-full rounded-[2.5rem] border border-blue-100 dark:border-blue-500/20 bg-blue-50/50 dark:bg-blue-500/5 backdrop-blur-md p-6 text-left">
               <div className="mb-3 flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400">
                   <AudioLines size={14} />
                </div>
                <h4 className="text-[11px] font-black uppercase tracking-[0.2em] text-blue-600 dark:text-blue-500">
                  Synthesized Response
                </h4>
              </div>
              <p className={`min-h-[60px] text-sm font-medium leading-relaxed ${response ? 'text-slate-800 dark:text-slate-200' : 'text-slate-400 dark:text-slate-600 italic'}`}>
                {response || 'Awaiting processing...'}
              </p>
            </div>
          </div>
          
          <div className="mt-8 flex items-center justify-center gap-2">
             <Zap size={14} className="text-blue-500" />
             <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 dark:text-slate-500">
                Curio AI Vocal Matrix Active
             </p>
          </div>

        </div>
      </div>
    </div>
  );
};

export default VoiceAssistant;
