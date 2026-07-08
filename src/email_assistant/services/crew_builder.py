from collections.abc import Sequence

from crewai import Agent, Crew, Process, Task


def build_crew(agents: Sequence[Agent], tasks: Sequence[Task]) -> Crew:
    return Crew(agents=list(agents), tasks=list(tasks), process=Process.sequential, verbose=True)
