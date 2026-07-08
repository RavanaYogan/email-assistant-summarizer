from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmailMessage:
    id: str
    sender: str
    subject: str
    snippet: str
