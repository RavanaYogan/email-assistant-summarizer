from crewai import LLM, Agent


def create_response_generator_agent(llm: LLM) -> Agent:
    return Agent(
        role="Response Generator",
        goal="Generate concise and professional email replies.",
        backstory=("You create professional email drafts based on " "email content and context."),
        llm=llm,
        verbose=True,
    )
