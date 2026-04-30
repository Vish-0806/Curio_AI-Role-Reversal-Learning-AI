import logging
from openai import AsyncOpenAI
from config.settings import settings

logger = logging.getLogger(__name__)

# Initialize the OpenAI async client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def text_to_speech(reply_text: str) -> bytes:
    """
    Optional: Converts text back to speech using OpenAI's TTS service.
    Returns the audio content as bytes.
    """
    try:
        logger.info("Converting text to speech...")
        
        response = await client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=reply_text
        )
        
        # Read the raw audio response
        audio_content = response.content
        logger.info("Text-to-speech conversion successful.")
        
        return audio_content
        
    except Exception as e:
        logger.error(f"Error during TTS conversion: {str(e)}")
        raise
