from crewai import LLM

llm = LLM(
    model="openai/BAI-IVision-SFT-3_2",
    base_url="https://table-extraction-llm.aptimeta.com/v1",
    api_key="dummy"
)

response = llm.call(
    "Classify this email: Meeting tomorrow at 10 AM"
)

print(response)