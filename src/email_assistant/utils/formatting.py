from collections.abc import Sequence

from email_assistant.models.email import EmailMessage


def format_emails_for_prompt(emails: Sequence[EmailMessage]) -> str:
    if not emails:
        return "No emails."

    return "\n".join(
        f"- id: {email.id}\n  from: {email.sender}\n  subject: {email.subject}\n  snippet: {email.snippet}"
        for email in emails
    )
