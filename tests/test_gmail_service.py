from pathlib import Path
from unittest.mock import MagicMock, patch

from email_assistant.services.gmail_service import GmailService


def _mock_service_with_messages() -> MagicMock:
    service = MagicMock()
    service.users.return_value.messages.return_value.list.return_value.execute.return_value = {
        "messages": [{"id": "abc123"}]
    }
    service.users.return_value.messages.return_value.get.return_value.execute.return_value = {
        "snippet": "Hello there",
        "payload": {
            "headers": [
                {"name": "From", "value": "sender@example.com"},
                {"name": "Subject", "value": "Test Subject"},
            ]
        },
    }
    return service


@patch("email_assistant.services.gmail_service.build")
@patch("email_assistant.services.gmail_service.Credentials")
def test_fetch_unread_returns_email_messages(
    mock_credentials: MagicMock, mock_build: MagicMock, tmp_path: Path
) -> None:
    token_path = tmp_path / "token.json"
    token_path.write_text("{}", encoding="utf-8")

    mock_credentials.from_authorized_user_file.return_value = MagicMock(valid=True)
    mock_build.return_value = _mock_service_with_messages()

    gmail = GmailService(
        credentials_path=tmp_path / "credentials.json",
        token_path=token_path,
    )
    emails = gmail.fetch_unread(max_results=1)

    assert len(emails) == 1
    assert emails[0].id == "abc123"
    assert emails[0].sender == "sender@example.com"
    assert emails[0].subject == "Test Subject"
    assert emails[0].snippet == "Hello there"


@patch("email_assistant.services.gmail_service.build")
@patch("email_assistant.services.gmail_service.Credentials")
def test_fetch_unread_empty_inbox(
    mock_credentials: MagicMock, mock_build: MagicMock, tmp_path: Path
) -> None:
    token_path = tmp_path / "token.json"
    token_path.write_text("{}", encoding="utf-8")

    mock_credentials.from_authorized_user_file.return_value = MagicMock(valid=True)

    service = MagicMock()
    service.users.return_value.messages.return_value.list.return_value.execute.return_value = {}
    mock_build.return_value = service

    gmail = GmailService(
        credentials_path=tmp_path / "credentials.json",
        token_path=token_path,
    )
    emails = gmail.fetch_unread(max_results=1)

    assert emails == []
