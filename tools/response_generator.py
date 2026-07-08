from tools.groq_tool import ask_groq

def generate_reply(email_data, tone="professional"):

    prompt = f"""
You are an Email Response Agent.

Generate a reply for the email below.

Email:
{email_data}

Tone:
{tone}

Rules:
- Be concise.
- Be relevant to the email.
- Generate only the email body.
- Do not include explanations.
- Do not mention that you are an AI.
"""

    return ask_groq(prompt)