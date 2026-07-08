from crewai import Agent, Task

from email_assistant.models.email import EmailMessage
from email_assistant.utils.formatting import format_emails_for_prompt


def create_classifier_task(agent: Agent, emails: list[EmailMessage]) -> Task:
    return Task(
        description=f"""
Classify the following emails.

Emails:
{format_emails_for_prompt(emails)}

Categories:
- IMPORTANT
- WORK
- PERSONAL
- PROMOTION
- SPAM

For each email provide:
- Category
- Importance
- Reason
""",
        expected_output="Email classification report.",
        agent=agent,
    )
