import logging
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

LOGGER = logging.getLogger(__name__)

def get_gmail_service():
    """
    Authenticate with Gmail and return a Gmail service client.
    """

    LOGGER.info("Initializing Gmail service")

    creds = None

    token_path = Path("token.json")
    credentials_path = Path("credentials.json")

    if token_path.exists():
        LOGGER.info("Loading existing token.json")

        creds = Credentials.from_authorized_user_file(
            token_path,
            SCOPES,
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            LOGGER.info("Refreshing Gmail token")

            creds.refresh(Request())

        else:

            LOGGER.info("Starting Gmail OAuth flow")

            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                SCOPES,
            )

            creds = flow.run_local_server(port=0)

        token_path.write_text(creds.to_json())

        LOGGER.info("token.json generated successfully")

    LOGGER.info("Gmail service initialized successfully")

    return build(
        "gmail",
        "v1",
        credentials=creds,
    )

def test_connection():
    """
    Verify Gmail connection.
    """

    LOGGER.info("Testing Gmail connection")

    service = get_gmail_service()

    profile = (
        service.users()
        .getProfile(userId="me")
        .execute()
    )

    LOGGER.info(
        "Connected to Gmail account: %s",
        profile["emailAddress"]
    )

    print("\nConnected Successfully")
    print(f"Email: {profile['emailAddress']}")

def get_unread_emails(max_results: int = 10):
    """
    Fetch unread emails from Gmail.
    """

    LOGGER.info(
        "Fetching unread emails (max_results=%s)",
        max_results
    )

    service = get_gmail_service()

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=["UNREAD"],
            maxResults=max_results,
        )
        .execute()
    )

    messages = results.get("messages", [])

    LOGGER.info(
        "Found %s unread emails",
        len(messages)
    )

    emails = []

    for index, message in enumerate(messages, start=1):

        LOGGER.info(
            "Processing email %s/%s",
            index,
            len(messages)
        )

        msg = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
            )
            .execute()
        )

        headers = msg.get("payload", {}).get("headers", [])

        sender = ""
        subject = ""

        for header in headers:

            if header["name"] == "From":
                sender = header["value"]

            elif header["name"] == "Subject":
                subject = header["value"]

        emails.append(
            {
                "id": message["id"],
                "sender": sender,
                "subject": subject,
                "snippet": msg.get("snippet", ""),
            }
        )

        LOGGER.info(
            "Email fetched | Sender=%s | Subject=%s",
            sender,
            subject,
        )

    LOGGER.info(
        "Successfully processed %s unread emails",
        len(emails)
    )

    return emails