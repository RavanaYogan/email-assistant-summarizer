from crewai import Crew, Process

def create_crew(
    reader_agent,
    classifier_agent,
    response_agent,
    reader_task,
    classifier_task,
    response_task,
):
    return Crew(
        agents=[
            reader_agent,
            classifier_agent,
            response_agent,
        ],
        tasks=[
            reader_task,
            classifier_task,
            response_task,
        ],
        process=Process.sequential,
        verbose=True,
    )