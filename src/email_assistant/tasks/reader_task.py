from crewai import Agent, Task

from email_assistant.models.email import EmailMessage
from email_assistant.utils.formatting import format_emails_for_prompt


def create_reader_task(agent: Agent, emails: list[EmailMessage]) -> Task:
    return Task(
        description=f"""
Review the following unread emails.

Emails:
{format_emails_for_prompt(emails)}

Return:
- Sender
- Subject
- Snippet
""",
        expected_output="Structured email overview.",
        agent=agent,
    )
