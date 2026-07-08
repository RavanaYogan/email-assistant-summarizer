from dataclasses import FrozenInstanceError

import pytest

from email_assistant.models.email import EmailMessage


def test_email_message_fields() -> None:
    email = EmailMessage(id="1", sender="a@b.com", subject="Hi", snippet="Hello")

    assert email.id == "1"
    assert email.sender == "a@b.com"
    assert email.subject == "Hi"
    assert email.snippet == "Hello"


def test_email_message_is_immutable() -> None:
    email = EmailMessage(id="1", sender="a@b.com", subject="Hi", snippet="Hello")

    with pytest.raises(FrozenInstanceError):
        email.id = "2"  # type: ignore[misc]
