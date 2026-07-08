# Email Assistant Using Crew AI

CrewAI-based assistant that reads unread Gmail messages, classifies them, and drafts replies using
an LLM.

## Features

- Fetches unread Gmail messages via the Gmail API (OAuth2, readonly scope)
- Classifies each email into IMPORTANT / WORK / PERSONAL / PROMOTION / SPAM using a CrewAI agent
- Drafts a professional reply for emails that need one
- Writes a run report to `logs/email_report.txt` and structured logs to `logs/app.log`
- Secrets are redacted from logs via a logging filter

## Folder structure

```
src/email_assistant/
    config/       # Settings (env loading) and logging setup
    models/       # EmailMessage dataclass, domain exceptions
    services/     # GmailService, EmailCacheService, crew builder
    tools/        # reserved for CrewAI @tool wrappers (none needed yet)
    agents/       # CrewAI Agent factories (reader, classifier, response generator)
    tasks/        # CrewAI Task factories
    cli/          # entry point (composition root)
tests/            # pytest suite
```

`EmailCacheService` (SQLite, `database/cache.db`) is a standalone service not yet wired into the
crew pipeline — it's available for future use (e.g. skipping re-classification of known emails).

## Installation

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```bash
uv sync
```

For contributing (lint/type/test tooling):

```bash
uv sync --group dev
pre-commit install
```

## Environment variables

Copy `.env.example` to `.env` and fill in real values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `CUSTOM_LLM_BASE_URL` | yes | OpenAI-compatible base URL for the LLM used by the crew agents |
| `CUSTOM_LLM_MODEL` | yes | Model name served at that endpoint |
| `CUSTOM_LLM_API_KEY` | yes | API key for that endpoint |
| `GMAIL_CREDENTIALS_PATH` | no | Path to Google OAuth client file (default `credentials.json`) |
| `GMAIL_TOKEN_PATH` | no | Path to the cached OAuth token (default `token.json`) |
| `LOG_DIR` | no | Log output directory (default `logs`) |
| `CACHE_DB_PATH` | no | SQLite cache path (default `database/cache.db`) |

You also need a Google Cloud OAuth client (Gmail API, readonly scope) downloaded as
`credentials.json` in the project root.

## Running locally

```bash
uv run email-assistant
# or
uv run python -m email_assistant.cli.main
```

First run opens a browser for Gmail OAuth consent and writes `token.json`.

## Example output

```
logs/app.log
2026-07-08 15:30:01 | INFO | email_assistant.cli.main | Starting Email Assistant
2026-07-08 15:30:01 | INFO | email_assistant.services.gmail_service | Fetching unread emails (max_results=3)
2026-07-08 15:30:02 | INFO | email_assistant.services.gmail_service | Found 2 unread emails
2026-07-08 15:30:04 | INFO | email_assistant.cli.main | Crew execution started
2026-07-08 15:30:18 | INFO | email_assistant.cli.main | Report saved to logs/email_report.txt
```

```
logs/email_report.txt
+--------------------------------------------------------------+
|                    EMAIL ASSISTANT REPORT                    |
+--------------------------------------------------------------+

... crew output: sender/subject/snippet, classification, draft reply ...

+--------------------------------------------------------------+
|                        END OF REPORT                         |
+--------------------------------------------------------------+
```

## Troubleshooting

- **`RefreshError: invalid_grant`** — the cached Gmail token was revoked or expired. Delete
  `token.json` and rerun; the app falls back to a fresh OAuth flow automatically.
- **`ConfigurationError: Missing required environment variables: ...`** — one of
  `CUSTOM_LLM_BASE_URL` / `CUSTOM_LLM_MODEL` / `CUSTOM_LLM_API_KEY` isn't set in `.env`.
- **`GmailAuthenticationError: Missing OAuth client file`** — `credentials.json` isn't in the
  project root (or wherever `GMAIL_CREDENTIALS_PATH` points).
- **No browser opens for OAuth** — `flow.run_local_server` needs a local browser; run this on a
  machine with one, or forward the port if running remotely.

## Testing

```bash
uv run pytest
```

## Secrets

`.env`, `credentials.json`, and `token.json` contain live secrets and are gitignored — never
commit them. See [SECURITY.md](SECURITY.md).
