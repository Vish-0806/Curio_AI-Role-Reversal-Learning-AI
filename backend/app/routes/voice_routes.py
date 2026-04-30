from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.whisper_service import transcribe_audio
from app.services.llm_service import get_llm_response
from app.services.tts_service import text_to_speech
from app.config.settings import get_settings
import logging

settings = get_settings()

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/voice-chat")
async def voice_chat(audio: UploadFile = File(...)):
    """
    Receives an audio file from the frontend, transcribes it, 
    gets a response from the LLM, and optionally converts it to speech.
    """
    try:
        # Validate the uploaded file
        if not audio.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Must be audio.")
            
        # 1. Transcribe audio using Whisper
        audio_content = await audio.read()
        transcript = await transcribe_audio(audio_content, audio.filename)
        
        if not transcript:
            raise HTTPException(status_code=400, detail="Failed to transcribe audio.")

        # 2. Get LLM response using GPT
        ai_response = await get_llm_response(transcript)
        
        # 3. Optional: Convert text to speech (if needed for backend TTS)
        # Note: Set ENABLE_BACKEND_TTS to True in settings to use OpenAI TTS
        audio_reply = None
        if hasattr(settings, "ENABLE_BACKEND_TTS") and settings.ENABLE_BACKEND_TTS:
            audio_reply = await text_to_speech(ai_response)
            # In a full implementation, you could return the audio as a streaming response
            # or save it and return a URL. For now, we return text.

        return {
            "status": "success",
            "transcript": transcript,
            "response": ai_response,
            "has_audio_reply": bool(audio_reply)
        }
        
    except Exception as e:
        logger.error(f"Error in voice_chat route: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during voice processing.")
