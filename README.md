# Email Assistant

CrewAI-based assistant that reads unread Gmail messages, classifies them, and drafts replies using an LLM.

## Architecture

- **agents/** — CrewAI agent definitions (reader, classifier, response generator)
- **tools/gmail_tool.py** — Gmail API auth + unread message fetch
- **tools/groq_tool.py**, **tools/email_classifier.py**, **tools/response_generator.py** — standalone Groq-based helpers (not wired into the main crew flow)
- **tasks.py** — CrewAI task definitions
- **crew.py** — assembles agents/tasks into a sequential `Crew`
- **database/cache.py** — SQLite cache for email classifications
- **logger_config.py** — logging setup (console + `logs/app.log`)
- **main.py** — entry point

## Setup

```bash
uv sync
cp .env.example .env   # fill in real values
```

Requires:
- Google Cloud OAuth client credentials saved as `credentials.json` (Gmail API, readonly scope)
- Groq API key
- Custom LLM endpoint (OpenAI-compatible)

## Run

```bash
uv run main.py
```

First run opens a browser for Gmail OAuth consent and writes `token.json`. If you see `RefreshError: invalid_grant`, delete `token.json` and rerun to re-authenticate.

## Output

- `logs/app.log` — structured log of each run
- `logs/email_report.txt` — final crew report (overwritten each run)

## Secrets

`.env`, `credentials.json`, and `token.json` contain live secrets and are gitignored. Never commit them.
