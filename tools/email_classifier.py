from tools.groq_tool import ask_groq

def classify_emails(emails):

    prompt = f"""
    You are an Email Classification Agent.

    Classify each email individually.

    Return ONLY this format:

    EMAIL 1
    Category:
    Importance:
    Reason:

    EMAIL 2
    Category:
    Importance:
    Reason:

    EMAIL 3
    Category:
    Importance:
    Reason:

Allowed Categories:
- IMPORTANT
- WORK
- PERSONAL
- PROMOTION
- SPAM

Allowed Importance:
- HIGH
- MEDIUM
- LOW

Do NOT:
- Analyze trends
- Give observations
- Give insights
- Give recommendations
- Give conclusions
- Mention sender distribution

Emails:
{emails}
"""
    return ask_groq(prompt)