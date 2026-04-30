import io
import os
import logging
from openai import AsyncOpenAI
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

# Initialize the OpenAI async client inside the function or globally with getter
settings = get_settings()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def transcribe_audio(audio_content: bytes, filename: str) -> str:
    """
    Transcribes audio bytes using OpenAI's Whisper model.
    Sends the audio blob directly to the backend without permanent file storage.
    """
    try:
        # Create an in-memory file-like object to send to the API
        audio_file = io.BytesIO(audio_content)
        audio_file.name = filename if filename else "audio.webm"
        
        logger.info("Sending audio to OpenAI Whisper API...")
        
        response = await client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="text"
        )
        
        logger.info("Audio transcription successful.")
        return response
    except Exception as e:
        logger.error(f"Error during audio transcription: {str(e)}")
        raise
