import logging
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
def ask_groq(prompt: str):

    LOGGER.info("Sending prompt to Groq (llama-3.3-70b-versatile)")

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    except Exception:
        LOGGER.exception("Groq API call failed")
        raise

    LOGGER.info("Groq response received")

    return response.choices[0].message.content

def summarize_emails(emails):

    prompt = f"""
    Analyze these emails:

    {emails}
    """

    return ask_groq(prompt)