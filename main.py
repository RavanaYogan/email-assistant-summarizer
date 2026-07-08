import os
from pathlib import Path
from dotenv import load_dotenv
from crewai import LLM
from logger_config import setup_logger
from tools.gmail_tool import get_unread_emails
from agents.email_reader import create_email_reader_agent
from agents.email_classifier import create_email_classifier_agent
from agents.response_generator import create_response_generator_agent
from tasks import (
    create_reader_task,
    create_classifier_task,
    create_response_task,
)
from crew import create_crew
from logger_config import setup_logger

setup_logger()
load_dotenv()

logger = setup_logger()

def main():

    logger.info("Starting Email Assistant")
    emails = get_unread_emails(max_results=3)
    logger.info(
        "Retrieved %s unread emails",
        len(emails)
    )

    llm = LLM(
    model=f"openai/{os.getenv('CUSTOM_LLM_MODEL')}",
    base_url=os.getenv("CUSTOM_LLM_BASE_URL"),
    api_key=os.getenv("CUSTOM_LLM_API_KEY")
    )

    logger.info("Custom LLM initialized")
    reader_agent = create_email_reader_agent(llm)
    classifier_agent = create_email_classifier_agent(llm)
    response_agent = create_response_generator_agent(llm)
    reader_task = create_reader_task(
        reader_agent,
        emails,
    )
    classifier_task = create_classifier_task(
        classifier_agent,
        emails,
    )
    response_task = create_response_task(
        response_agent,
        emails,
    )

    crew = create_crew(
        reader_agent,
        classifier_agent,
        response_agent,
        reader_task,
        classifier_task,
        response_task,
    )

    logger.info("Crew execution started")
    result = crew.kickoff()

    report = f"""
+--------------------------------------------------------------+
|                    EMAIL ASSISTANT REPORT                    |
+--------------------------------------------------------------+

{result}

+--------------------------------------------------------------+
|                        END OF REPORT                         |
+--------------------------------------------------------------+
"""

    Path("logs/email_report.txt").write_text(report, encoding="utf-8")

    logger.info("Report saved to logs/email_report.txt")
    logger.info("Final Result:\n%s", result)

if __name__ == "__main__":
    main()