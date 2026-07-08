from crewai import Agent, Task

from email_assistant.models.email import EmailMessage
from email_assistant.utils.formatting import format_emails_for_prompt


def create_response_task(agent: Agent, emails: list[EmailMessage]) -> Task:
    return Task(
        description=f"""
Generate professional reply drafts for emails
that require a response.

Emails:
{format_emails_for_prompt(emails)}
""",
        expected_output="Professional email draft.",
        agent=agent,
    )
