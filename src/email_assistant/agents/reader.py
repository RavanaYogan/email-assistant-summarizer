from crewai import LLM, Agent


def create_email_reader_agent(llm: LLM) -> Agent:
    return Agent(
        role="Email Reader",
        goal="Read unread Gmail messages and present them clearly.",
        backstory=("You review unread Gmail messages and prepare them " "for further processing."),
        llm=llm,
        verbose=True,
    )
