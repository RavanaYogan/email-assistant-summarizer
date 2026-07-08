from crewai import Agent

def create_response_generator_agent(llm):
    return Agent(
        role="Response Generator",
        goal="Generate concise and professional email replies.",
        backstory=(
            "You create professional email drafts based on "
            "email content and context."
        ),
        llm=llm,
        verbose=True,
    )