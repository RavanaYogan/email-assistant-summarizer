from email_assistant.models.email import EmailMessage
from email_assistant.utils.formatting import format_emails_for_prompt


def test_format_emails_for_prompt_empty() -> None:
    assert format_emails_for_prompt([]) == "No emails."


def test_format_emails_for_prompt_includes_fields() -> None:
    email = EmailMessage(id="1", sender="a@b.com", subject="Hi", snippet="Hello")

    formatted = format_emails_for_prompt([email])

    assert "a@b.com" in formatted
    assert "Hi" in formatted
    assert "Hello" in formatted
