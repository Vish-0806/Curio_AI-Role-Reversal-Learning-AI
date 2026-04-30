import logging
from openai import AsyncOpenAI
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def get_llm_response(user_text: str) -> str:
    """
    Sends the transcribed text to GPT (gpt-4o-mini) to generate an intelligent response.
    """
    try:
        logger.info(f"Sending text to LLM: {user_text}")
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful, concise voice assistant. Respond naturally and briefly as if speaking."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        ai_reply = response.choices[0].message.content
        logger.info("LLM response generated successfully.")
        return ai_reply
        
    except Exception as e:
        logger.error(f"Error generating LLM response: {str(e)}")
        raise
