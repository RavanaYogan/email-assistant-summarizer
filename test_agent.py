from crewai import Agent
from crewai import LLM

llm = LLM(
    model="openai/BAI-IVision-SFT-3_2",
    base_url="https://table-extraction-llm.aptimeta.com/v1",
    api_key="dummy"
)

agent = Agent(
    role="Email Classifier",
    goal="Classify emails",
    backstory="Expert email analyst",
    llm=llm,
    verbose=True
)

result = agent.execute_task(
    "Classify: Meeting tomorrow at 10 AM"
)

print(result)