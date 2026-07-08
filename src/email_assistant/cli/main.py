import logging
import sys
from pathlib import Path

from crewai import LLM

from email_assistant.agents.classifier import create_email_classifier_agent
from email_assistant.agents.reader import create_email_reader_agent
from email_assistant.agents.response_generator import create_response_generator_agent
from email_assistant.config.logging_config import configure_logging
from email_assistant.config.settings import Settings
from email_assistant.models.exceptions import EmailAssistantError
from email_assistant.services.crew_builder import build_crew
from email_assistant.services.gmail_service import GmailService
from email_assistant.tasks.classifier_task import create_classifier_task
from email_assistant.tasks.reader_task import create_reader_task
from email_assistant.tasks.response_task import create_response_task

logger = logging.getLogger(__name__)

MAX_UNREAD_EMAILS = 3


def _build_llm(settings: Settings) -> LLM:
    return LLM(
        model=f"openai/{settings.custom_llm_model}",
        base_url=settings.custom_llm_base_url,
        api_key=settings.custom_llm_api_key,
    )


def _write_report(log_dir: Path, result: object) -> None:
    report = f"""
+--------------------------------------------------------------+
|                    EMAIL ASSISTANT REPORT                    |
+--------------------------------------------------------------+

{result}

+--------------------------------------------------------------+
|                        END OF REPORT                         |
+--------------------------------------------------------------+
"""
    report_path = log_dir / "email_report.txt"
    report_path.write_text(report, encoding="utf-8")
    logger.info("Report saved to %s", report_path)


def run() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    try:
        settings = Settings.from_env()
    except EmailAssistantError:
        logger.exception("Configuration error")
        return 1

    configure_logging(settings.log_dir, sensitive_values=settings.secrets)
    logger.info("Starting Email Assistant")

    try:
        gmail = GmailService(settings.gmail_credentials_path, settings.gmail_token_path)
        emails = gmail.fetch_unread(max_results=MAX_UNREAD_EMAILS)
        logger.info("Retrieved %s unread emails", len(emails))

        llm = _build_llm(settings)
        logger.info("Custom LLM initialized")

        reader_agent = create_email_reader_agent(llm)
        classifier_agent = create_email_classifier_agent(llm)
        response_agent = create_response_generator_agent(llm)

        crew = build_crew(
            agents=[reader_agent, classifier_agent, response_agent],
            tasks=[
                create_reader_task(reader_agent, emails),
                create_classifier_task(classifier_agent, emails),
                create_response_task(response_agent, emails),
            ],
        )

        logger.info("Crew execution started")
        result = crew.kickoff()
    except EmailAssistantError:
        logger.exception("Email assistant pipeline failed")
        return 1
    except Exception:
        logger.exception("Unexpected failure in email assistant pipeline")
        return 1

    _write_report(settings.log_dir, result)
    logger.info("Final result:\n%s", result)
    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
