import logging
from collections.abc import Sequence
from pathlib import Path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

from email_assistant.models.email import EmailMessage
from email_assistant.models.exceptions import GmailAuthenticationError, GmailServiceError

logger = logging.getLogger(__name__)

DEFAULT_SCOPES: tuple[str, ...] = ("https://www.googleapis.com/auth/gmail.readonly",)


class GmailService:
    def __init__(
        self,
        credentials_path: Path,
        token_path: Path,
        scopes: Sequence[str] = DEFAULT_SCOPES,
    ) -> None:
        self._credentials_path = credentials_path
        self._token_path = token_path
        self._scopes = list(scopes)
        self._service: Resource | None = None

    def _load_credentials(self) -> Credentials:
        creds: Credentials | None = None

        if self._token_path.exists():
            logger.debug("Loading existing token from %s", self._token_path)
            creds = Credentials.from_authorized_user_file(str(self._token_path), self._scopes)

        if creds and creds.valid:
            return creds

        if creds and creds.expired and creds.refresh_token:
            try:
                logger.info("Refreshing Gmail token")
                creds.refresh(Request())
                self._token_path.write_text(creds.to_json(), encoding="utf-8")
                return creds
            except RefreshError:
                logger.warning("Token refresh failed; starting new OAuth flow")
                creds = None

        if not self._credentials_path.exists():
            raise GmailAuthenticationError(f"Missing OAuth client file: {self._credentials_path}")

        logger.info("Starting Gmail OAuth flow")
        flow = InstalledAppFlow.from_client_secrets_file(str(self._credentials_path), self._scopes)
        creds = flow.run_local_server(port=0)
        self._token_path.write_text(creds.to_json(), encoding="utf-8")
        logger.info("Token saved to %s", self._token_path)
        return creds

    def _get_service(self) -> Resource:
        if self._service is None:
            try:
                creds = self._load_credentials()
                self._service = build("gmail", "v1", credentials=creds)
            except RefreshError as exc:
                logger.exception("Gmail authentication failed")
                raise GmailAuthenticationError("Gmail authentication failed") from exc
        return self._service

    def test_connection(self) -> str:
        try:
            service = self._get_service()
            profile = service.users().getProfile(userId="me").execute()
        except HttpError as exc:
            logger.exception("Gmail connection test failed")
            raise GmailServiceError("Failed to verify Gmail connection") from exc

        email_address: str = profile["emailAddress"]
        logger.info("Connected to Gmail account: %s", email_address)
        return email_address

    def fetch_unread(self, max_results: int = 10) -> list[EmailMessage]:
        logger.info("Fetching unread emails (max_results=%s)", max_results)

        try:
            service = self._get_service()
            results = (
                service.users()
                .messages()
                .list(userId="me", labelIds=["UNREAD"], maxResults=max_results)
                .execute()
            )
        except HttpError as exc:
            logger.exception("Failed to list unread messages")
            raise GmailServiceError("Failed to list unread messages") from exc

        message_refs = results.get("messages", [])
        logger.info("Found %s unread emails", len(message_refs))

        emails: list[EmailMessage] = []
        for index, message_ref in enumerate(message_refs, start=1):
            logger.debug("Fetching email %s/%s", index, len(message_refs))
            try:
                msg = service.users().messages().get(userId="me", id=message_ref["id"]).execute()
            except HttpError:
                logger.exception("Failed to fetch message %s; skipping", message_ref["id"])
                continue

            headers = msg.get("payload", {}).get("headers", [])
            sender = next((h["value"] for h in headers if h["name"] == "From"), "")
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")

            emails.append(
                EmailMessage(
                    id=message_ref["id"],
                    sender=sender,
                    subject=subject,
                    snippet=msg.get("snippet", ""),
                )
            )
            logger.debug("Email fetched | sender=%s | subject=%s", sender, subject)

        logger.info("Successfully processed %s unread emails", len(emails))
        return emails
